from django.urls import path
from .views import shop, add_product, product_detail,cart,add_to_cart

urlpatterns = [
    path("shop/", shop, name="shop"),
    path("add/", add_product, name="add_product"),
    path("product/<str:product_id>/", product_detail, name="product_detail"),
    path("add-to-cart/<str:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
]

