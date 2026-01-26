from django.urls import path
from .views import shop, add_product, product_detail,cart,add_to_cart,increase_qty,decrease_qty,cart_count_api,checkout,order_success

urlpatterns = [
    path("shop/", shop, name="shop"),
    path("add/", add_product, name="add_product"),
    path("product/<str:product_id>/", product_detail, name="product_detail"),
    path("add-to-cart/<str:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("cart/increase/<str:item_id>/", increase_qty, name="increase_qty"),
    path("cart/decrease/<str:item_id>/", decrease_qty, name="decrease_qty"),
    path('api/cart-count/', cart_count_api, name='cart_count_api'),
    path("checkout/", checkout, name="checkout"),
    path("order-success/", order_success, name="order_success"),


]

