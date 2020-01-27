from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path(r"", views.index),
    path("products", views.ProductList.as_view(), name="list"),
    path("product/<int:pk>/", views.ProductDetail.as_view(), name="detail"),
]
