from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import random


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def send_verification_email(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.save()
        send_mail(
            "Подтверждение регистрации",
            f"Ваш код подтверждения: {self.verification_code}",
            "no-reply@messageboard.com",
            [self.email]
        )


class Category(models.TextChoices):
    TANKS = "Танки", _("Танки")
    HEALERS = "Хилы", _("Хилы")
    DPS = "ДД", _("ДД")
    TRADERS = "Торговцы", _("Торговцы")
    GUILD_MASTERS = "Гилдмастеры", _("Гилдмастеры")
    QUEST_GIVERS = "Квестгиверы", _("Квестгиверы")
    BLACKSMITHS = "Кузнецы", _("Кузнецы")
    LEATHERWORKERS = "Кожевники", _("Кожевники")
    ALCHEMISTS = "Зельевары", _("Зельевары")
    SPELL_MASTERS = "Мастера заклинаний", _("Мастера заклинаний")


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Response(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def accept(self):
        self.accepted = True
        self.save()
        send_mail(
            "Ваш отклик принят!",
            f"Ваш отклик на объявление '{self.listing.title}' был принят!",
            "no-reply@messageboard.com",
            [self.user.email]
        )