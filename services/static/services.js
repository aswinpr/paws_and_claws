let currentService = "";

function openBooking(type) {
  currentService = type;
  document.getElementById("bookingModal").style.display = "flex";

  document.getElementById("timeSlotField").style.display =
    type === "grooming" ? "block" : "none";

  document.getElementById("endDateField").style.display =
    type === "hostel" ? "block" : "none";

  document.getElementById("modalTitle").innerText =
    type === "grooming" ? "Book Grooming" : "Book Hostel";
}

function closeBooking() {
  document.getElementById("bookingModal").style.display = "none";
}

document.getElementById("bookingForm").addEventListener("submit", function (e) {
  e.preventDefault();
  alert("Booking Confirmed 🎉");
  closeBooking();
});
