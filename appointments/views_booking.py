from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware

from .forms_booking import BookingSearchForm
from .models import Appointment, StaffProfile
from .utils import generate_slots

@login_required
def book_appointment(request):
    if request.user.role != "CLIENT":
        return render(request, "403.html", status=403)

    slots = []
    form = BookingSearchForm(request.GET or None)

    if form.is_valid():
        service = form.cleaned_data["service"]
        staff = form.cleaned_data["staff"]
        date = form.cleaned_data["date"]

        slots = generate_slots(staff, service, date)

        if request.method == "POST":
            start = request.POST.get("start")
            end = request.POST.get("end")

            Appointment.objects.create(
                client=request.user,
                staff=staff,
                service=service,
                start_dt=make_aware(start),
                end_dt=make_aware(end),
            )
            messages.success(request, "Termin je rezerviran.")
            return redirect("my_appointments")

    return render(request, "booking/book.html", {
        "form": form,
        "slots": slots,
    })
