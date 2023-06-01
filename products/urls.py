from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("products/<int:_id>/", views.detail_view),
    path("products/<int:_id>/inventory", views.inventory_view),
    path("products/register/", views.register),
    path("products/<int:_id>/delete/", views.delete),
    path("products/order/", views.order),
    path("products/<int:_id>/inbound", views.inbound),
    path("products/<int:_id>/outbound", views.outbound),
]
