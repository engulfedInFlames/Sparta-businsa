from django.urls import path
from . import views


urlpatterns = [
    path("profile/<int:_id>", views.show_profile),
    path("sign-in/", views.signin),
    path("sign-up/", views.signup),
    path("logout/", views.logout)
]
