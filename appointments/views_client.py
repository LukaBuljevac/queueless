from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appointment

@login_required
def my_appointments(request):
    appts = Appointment.objects.filter(client=request.user).order_by("-start_dt")
    return render(request, "booking/my_appointments.html", {"appointments": appts})
