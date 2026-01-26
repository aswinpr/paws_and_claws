from django.shortcuts import render,redirect
from datetime import datetime
from .db import bookings_collection
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from bson import ObjectId
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.
@login_required(login_url='login')
def services(request):
    return render(request, 'services/services.html')

def dog_grooming(request):
    return render(request,'services/dog_groom.html')

def cat_grooming(request):
    return render(request,'services/catgroom.html')

def pet_boarding(request):
    return render(request,'services/pet_boarding.html')


@login_required(login_url='login')
def create_booking(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"})

    try:
        data = json.loads(request.body)
        print("📦 Booking Data:", data)

        booking = {
            "user_id": request.user.id,
            "service_type": data.get("service_type"),
            "package_name": data.get("package_name"),
            "price": int(data.get("price") or 0),
            "pet_name": data.get("pet_name"),
            "pet_type": data.get("pet_type"),
            "start_date": data.get("start_date"),
            "time_slot": data.get("time_slot"),
            "notes": data.get("notes"),
            "created_at": datetime.now()
        }

        bookings_collection.insert_one(booking)

        return JsonResponse({"success": True})

    except Exception as e:
        print("❌ Booking Error:", str(e))
        return JsonResponse({"success": False, "message": str(e)})



@login_required(login_url='login')
def my_bookings(request):
    user_id = request.user.id

    raw_bookings = list(bookings_collection.find({"user_id": user_id}))

    bookings = []
    for b in raw_bookings:
        b["id"] = str(b["_id"])   # ✅ safe field
        del b["_id"]              # remove unsafe key
        bookings.append(b)

    return render(request, "services/my_bookings.html", {
        "bookings": bookings
    })



@login_required(login_url='login')
@require_POST
def cancel_booking(request, booking_id):
    try:
        user_id = request.user.id

        # Validate ObjectId
        if not ObjectId.is_valid(booking_id):
            return JsonResponse({
                "success": False,
                "message": "Invalid booking ID"
            })

        result = bookings_collection.delete_one({
            "_id": ObjectId(booking_id),
            "user_id": user_id
        })

        if result.deleted_count == 1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({
                "success": False,
                "message": "Booking not found"
            })

    except Exception as e:
        print("Cancel Error:", e)   # 👈 THIS WILL SHOW REAL ERROR
        return JsonResponse({
            "success": False,
            "message": "Server error"
        })

@staff_member_required
def admin_all_bookings(request):
    bookings = list(bookings_collection.find().sort("created_at", -1))

    # Convert ObjectId to string for templates
    for b in bookings:
        b["id"] = str(b["_id"])

    return render(request, "services/admin_all_bookings.html", {
        "bookings": bookings
    })


@staff_member_required
def admin_cancel_booking(request, booking_id):
    try:
        result = bookings_collection.delete_one({
            "_id": ObjectId(booking_id)
        })

        if result.deleted_count == 1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Booking not found"})

    except Exception as e:
        print("Admin Cancel Error:", e)
        return JsonResponse({"success": False, "message": "Server error"})
