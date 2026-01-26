from django.http import HttpResponse, Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from bson import ObjectId
from .db import products_collection, cart_collection,orders_collection
from datetime import datetime




# @login_required(login_url='login')
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

    product = products_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    # ❌ Product not found
    if not product:
        return redirect("shop")

    # ❌ Out of stock
    if product.get("stock", 0) <= 0:
        return redirect("shop")  # later show message

    cart_item = cart_collection.find_one({
        "user_id": user_id,
        "product_id": product["_id"]
    })

    if cart_item:
        # Increase cart quantity
        cart_collection.update_one(
            {"_id": cart_item["_id"]},
            {"$inc": {"quantity": 1}}
        )
    else:
        # Add new item to cart
        cart_collection.insert_one({
            "user_id": user_id,
            "product_id": product["_id"],
            "name": product["name"],
            "price": product["price"],
            "image": product.get("image"),
            "quantity": 1
        })

    # ✅ REDUCE STOCK BY 1
    products_collection.update_one(
        {"_id": product["_id"]},
        {"$inc": {"stock": -1}}
    )

    return redirect("cart")


@login_required(login_url='login')
def cart(request):
    user_id = request.user.id
    items = list(cart_collection.find({"user_id": user_id}))

    total = 0
    for item in items:
        item["id"] = str(item["_id"])
        del item["_id"]

        item["subtotal"] = item["price"] * item["quantity"]
        total += item["subtotal"]

    return render(request, "products/cart.html", {
        "items": items,
        "total": total
    })



@login_required(login_url='login')
def increase_qty(request, item_id):
    cart_item = cart_collection.find_one({"_id": ObjectId(item_id)})

    if not cart_item:
        return redirect("cart")

    product = products_collection.find_one(
        {"_id": cart_item["product_id"]}
    )

    # Check stock
    if product["stock"] <= 0:
        return redirect("cart")

    # Increase cart quantity
    cart_collection.update_one(
        {"_id": cart_item["_id"]},
        {"$inc": {"quantity": 1}}
    )

    # Reduce product stock
    products_collection.update_one(
        {"_id": product["_id"]},
        {"$inc": {"stock": -1}}
    )

    return redirect("cart")



@login_required(login_url='login')
def decrease_qty(request, item_id):
    cart_item = cart_collection.find_one({"_id": ObjectId(item_id)})

    if not cart_item:
        return redirect("cart")

    # Restore stock
    products_collection.update_one(
        {"_id": cart_item["product_id"]},
        {"$inc": {"stock": 1}}
    )

    if cart_item["quantity"] > 1:
        cart_collection.update_one(
            {"_id": cart_item["_id"]},
            {"$inc": {"quantity": -1}}
        )
    else:
        # Remove item if quantity becomes 0
        cart_collection.delete_one({"_id": cart_item["_id"]})

    return redirect("cart")



@login_required
def cart_count_api(request):
    user_id = request.user.id
    items = cart_collection.find({"user_id": user_id})

    total_qty = 0
    for item in items:
        total_qty += item.get("quantity", 1)

    return JsonResponse({
        "cart_count": total_qty
    })

@login_required
def checkout(request):
    user_id = request.user.id

    # 🔥 Get cart from MongoDB (NOT session)
    cart_items = list(cart_collection.find({"user_id": user_id}))

    if not cart_items:
        return redirect("cart")

    items = []
    total = 0

    for item in cart_items:
        subtotal = item["price"] * item["quantity"]
        total += subtotal

        items.append({
            "product_id": str(item["product_id"]),
            "name": item["name"],
            "price": item["price"],
            "qty": item["quantity"],
            "subtotal": subtotal
        })

    if request.method == "POST":
        order = {
            "user_id": user_id,
            "items": items,
            "total_amount": total,
            "shipping_name": request.POST.get("name"),
            "shipping_phone": request.POST.get("phone"),
            "shipping_address": request.POST.get("address"),
            "status": "Pending",
            "created_at": datetime.now()
        }

        orders_collection.insert_one(order)

        # 🔥 Clear cart from MongoDB
        cart_collection.delete_many({"user_id": user_id})

        return redirect("order_success")

    return render(request, "products/checkout.html", {
        "items": items,
        "total": total
    })

@login_required
def order_success(request):
    return render(request, "products/order_success.html")
