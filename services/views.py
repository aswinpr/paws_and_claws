from django.shortcuts import render,redirect
from datetime import datetime
from .db import bookings_collection
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse


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







