console.log("✅ services.js loaded");
let selectedService = "";
let selectedPackage = "";
let selectedPrice = 0;

// ================================
// OPEN BOOKING MODAL
// ================================
function openBookingModal(serviceType, packageName, price) {
  selectedService = serviceType;
  selectedPackage = packageName;
  selectedPrice = price;

  document.getElementById("modalTitle").textContent =
    "Book " + packageName;

  document.getElementById("serviceTypeInput").value = serviceType;
  document.getElementById("packageInput").value = packageName;
  document.getElementById("priceInput").value = price;

  document.getElementById("bookingModal").style.display = "flex";
}

// ================================
// CLOSE MODAL
// ================================
function closeBooking() {
  document.getElementById("bookingModal").style.display = "none";
}

// ================================
// FORM SUBMIT
// ================================
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("bookingForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const data = {
      service_type: selectedService,
      package_name: selectedPackage,
      price: selectedPrice,
      pet_name: document.getElementById("petName").value,
      pet_type: document.getElementById("petType").value,
      start_date: document.getElementById("startDate").value,
      time_slot: document.getElementById("timeSlot").value,
      notes: document.getElementById("notes").value
    };

    console.log("🚀 Sending:", data);

    fetch("/services/create-booking/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(result => {
        console.log("✅ Result:", result);
        if (result.success) {
          alert("Booking confirmed!");
          closeBooking();
        } else {
          alert("Error: " + result.message);
        }
      })
      .catch(err => {
        console.error(err);
        alert("Server error");
      });
  });
});

// ================================
// CSRF TOKEN
// ================================
function getCSRFToken() {
  let cookieValue = null;
  const name = "csrftoken";
  if (document.cookie) {
    const cookies = document.cookie.split(";");
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(c.substring(name.length + 1));
      }
    }
  }
  return cookieValue;
}
