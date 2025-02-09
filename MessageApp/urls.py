from django.urls import path
from .views import (
    register, verify_email, login_user, home,
    respond_to_listing, accept_response, delete_response, send_newsletter, create_listing, listing_detail, user_responses
)

urlpatterns = [
    path("register/", register, name="register"),
    path("verify-email/", verify_email, name="verify_email"),
    path("login/", login_user, name="login"),
    path("", home, name="home"),
    path("respond/<int:listing_id>/", respond_to_listing, name="respond_to_listing"),
    path("responses/<int:response_id>/accept/", accept_response, name="accept_response"),
    path("responses/<int:response_id>/delete/", delete_response, name="delete_response"),
    path("newsletter/", send_newsletter, name="send_newsletter"),
    path("create-listing/", create_listing, name="create_listing"),
    path("<int:listing_id>/", listing_detail, name="listing_detail"),
    path("responses/", user_responses, name="user_responses"),
    path("responses/<int:response_id>/accept/", accept_response, name="accept_response"),
    path("responses/<int:response_id>/delete/", delete_response, name="delete_response"),
]
