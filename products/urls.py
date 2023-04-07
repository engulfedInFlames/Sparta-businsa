from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("products/<int:_id>/", views.show_detail),
    path("products/register/", views.register),
    path("products/<int:_id>/delete/", views.delete),
    path("products/<int:_id>/inventory", views.inventory),
    path("products/<int:_id>/inbound", views.inbound),
    path("products/<int:_id>/outbound", views.outbound),
    path("products/order/", views.order),
]
