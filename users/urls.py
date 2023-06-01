from django.urls import path
from . import views


urlpatterns = [
    path("sign-up/", views.signup),
    path("sign-in/", views.login),
    path("logout/", views.logout),
    path("profile/<int:_id>", views.profile),
]
