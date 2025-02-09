from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .models import Listing, Response
from .forms import CustomUserCreationForm, ListingForm
import json

User = get_user_model()

def home(request):
    listings = Listing.objects.all()
    return render(request, "MessageApp/home.html", {"listings": listings})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_email_verified = False
            user.save()
            user.send_verification_email()
            return redirect("verify_email")
    else:
        form = CustomUserCreationForm()
    return render(request, "MessageApp/register.html", {"form": form})


def verify_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")
        user = User.objects.filter(email=email, verification_code=code).first()
        if user:
            user.is_email_verified = True
            user.verification_code = None
            user.save()
            login(request, user)
            return redirect("home")
        else:
            return render(request, "MessageApp/verify_email.html", {"error": "Неверный код"})
    return render(request, "MessageApp/verify_email.html")



def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "MessageApp/login.html", {"form": form})


def home(request):
    listings = Listing.objects.all()
    return render(request, "MessageApp/home.html", {"listings": listings})

@login_required
@csrf_exempt
def respond_to_listing(request, listing_id):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text")

        if not text:
            return JsonResponse({"error": "Текст отклика обязателен"}, status=400)

        listing = Listing.objects.get(id=listing_id)
        response = Response.objects.create(user=request.user, listing=listing, text=text)

        send_mail(
            "Новый отклик на ваше объявление",
            f"Вы получили новый отклик на '{listing.title}' от {request.user.username}.\n\n{text}",
            "no-reply@messageboard.com",
            [listing.user.email]
        )

        return JsonResponse({"message": "Отклик отправлен"})


@login_required
def accept_response(request, response_id):
    response = Response.objects.get(id=response_id, listing__user=request.user)
    response.accept()

    send_mail(
        "Ваш отклик принят!",
        f"Ваш отклик на '{response.listing.title}' был принят!",
        "no-reply@messageboard.com",
        [response.user.email]
    )

    return JsonResponse({"message": "Отклик принят"})


@login_required
def delete_response(request, response_id):
    response = Response.objects.get(id=response_id, listing__user=request.user)
    response.delete()
    return JsonResponse({"message": "Отклик удален"})


@login_required
def send_newsletter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        subject = data.get("subject")
        message = data.get("message")

        if not subject or not message:
            return JsonResponse({"error": "Тема и сообщение обязательны"}, status=400)

        recipients = User.objects.filter(is_email_verified=True).values_list("email", flat=True)
        send_mail(subject, message, "newsletters@messageboard.com", recipients)

        return JsonResponse({"message": "Рассылка отправлена"})


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect("home")
    else:
        form = ListingForm()

    return render(request, "MessageApp/create_listing.html", {"form": form})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        if request.user.is_authenticated:
            response_text = request.POST.get("response_text")
            if response_text:
                response = Response.objects.create(user=request.user, listing=listing, text=response_text)
                # Отправка уведомления владельцу объявления
                send_mail(
                    "Новый отклик на ваше объявление",
                    f"Вы получили новый отклик на '{listing.title}' от {request.user.username}.\n\n{response_text}",
                    "no-reply@messageboard.com",
                    [listing.user.email]
                )
                return redirect("listing_detail", listing_id=listing.id)

    return render(request, "MessageApp/listing_detail.html", {"listing": listing})


# Приватная страница откликов
@login_required
def user_responses(request):
    listing_id = request.GET.get("listing_id")
    user_listings = Listing.objects.filter(user=request.user)
    responses = Response.objects.filter(listing__user=request.user)

    if listing_id:
        responses = responses.filter(listing_id=listing_id)

    return render(request, "MessageApp/user_responses.html", {"responses": responses, "user_listings": user_listings})


# Принять отклик
@login_required
def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, listing__user=request.user)
    response.accept()

    # Уведомление отправителю
    send_mail(
        "Ваш отклик принят!",
        f"Ваш отклик на '{response.listing.title}' был принят!",
        "no-reply@messageboard.com",
        [response.user.email]
    )

    return redirect("user_responses")


# Удалить отклик
@login_required
@csrf_exempt
def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id, listing__user=request.user)
    response.delete()
    return redirect("user_responses")