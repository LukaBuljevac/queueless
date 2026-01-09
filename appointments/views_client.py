from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Appointment
from .permissions import client_required
from .rules import can_client_cancel

@login_required
@client_required
def my_appointments(request):
    appts = Appointment.objects.filter(client=request.user).order_by("-start_dt")
    return render(request, "booking/my_appointments.html", {"appointments": appts})

@login_required
@client_required
def cancel_appointment(request, pk: int):
    appt = get_object_or_404(Appointment, pk=pk, client=request.user)

    if request.method != "POST":
        return redirect("my_appointments")

    if not can_client_cancel(appt):
        messages.error(request, "Ovaj termin se više ne može otkazati (pravilo 24h ili status).")
        return redirect("my_appointments")

    appt.status = Appointment.Status.CANCELLED
    appt.save(update_fields=["status"])
    messages.success(request, "Termin je otkazan.")
    return redirect("my_appointments")
