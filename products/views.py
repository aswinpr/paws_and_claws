from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from bson import ObjectId
from .db import products_collection, cart_collection

@login_required(login_url='login')
def shop(request):
    products = list(products_collection.find())
    # Convert ObjectId to string for each product
    for product in products:
        product['id'] = str(product['_id'])
    return render(request, "products/shop.html", {"products": products})

 
@login_required(login_url='login')
def add_product(request):

    # 🔒 Admin check
    if not request.user.is_staff:
        return redirect("shop")

    if request.method == "POST":
        product = {
            "name": request.POST.get("name"),
            "price": int(request.POST.get("price")),
            "category": request.POST.get("category"),
            "stock": int(request.POST.get("stock")),
            "image": request.POST.get("image"),
            "description": request.POST.get("description"),
        }

        products_collection.insert_one(product)
        return redirect("shop")

    return render(request, "products/add_product.html")


@login_required(login_url='login')
def product_detail(request, product_id):
    product = products_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    return render(request, "products/product_detail.html", {
        "product": product
    })




@login_required(login_url='login')
def add_to_cart(request, product_id):
    user_id = request.user.id

    product = products_collection.find_one({"_id": ObjectId(product_id)})

    if not product:
        return redirect("shop")

    cart_item = cart_collection.find_one({
        "user_id": user_id,
        "product_id": product["_id"]
    })

    if cart_item:
        cart_collection.update_one(
            {"_id": cart_item["_id"]},
            {"$inc": {"quantity": 1}}
        )
    else:
        cart_collection.insert_one({
            "user_id": user_id,
            "product_id": product["_id"],
            "name": product["name"],
            "price": product["price"],
            "image": product["image"],
            "quantity": 1
        })

    return redirect("cart")


@login_required(login_url='login')
def cart(request):
    user_id = request.user.id
    items = list(cart_collection.find({"user_id": user_id}))

    total = sum(item["price"] * item["quantity"] for item in items)

    return render(request, "products/cart.html", {
        "items": items,
        "total": total
    })
