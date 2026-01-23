from .db import cart_collection
from django.contrib.auth.models import AnonymousUser

def cart_item_count(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        items = cart_collection.find({"user_id": user_id})

        total_qty = 0
        for item in items:
            total_qty += item.get("quantity", 1)

        return {"cart_count": total_qty}

    return {"cart_count": 0}
