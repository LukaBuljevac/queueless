from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Appointment, StaffProfile
from .permissions import staff_required

@login_required
@staff_required
def staff_requests(request):
    staff = StaffProfile.objects.get(user=request.user)
    appts = Appointment.objects.filter(staff=staff, status=Appointment.Status.PENDING).order_by("start_dt")
    return render(request, "staff/requests.html", {"appointments": appts})

@login_required
@staff_required
def staff_schedule_today(request):
    staff = StaffProfile.objects.get(user=request.user)
    today = timezone.localdate()
    appts = Appointment.objects.filter(
        staff=staff,
        start_dt__date=today,
        status__in=[Appointment.Status.APPROVED, Appointment.Status.PENDING],
    ).order_by("start_dt")
    return render(request, "staff/today.html", {"appointments": appts, "today": today})

@login_required
@staff_required
@transaction.atomic
def staff_approve(request, pk: int):
    staff = StaffProfile.objects.get(user=request.user)
    appt = get_object_or_404(Appointment, pk=pk, staff=staff)

    if request.method != "POST":
        return redirect("staff_requests")

    if appt.status != Appointment.Status.PENDING:
        messages.error(request, "Termin nije u statusu PENDING.")
        return redirect("staff_requests")

    # zaštita od konflikta (ako je netko drugi rezervirao u međuvremenu)
    conflict = Appointment.objects.select_for_update().filter(
        staff=staff,
        status=Appointment.Status.APPROVED,
        start_dt__lt=appt.end_dt,
        end_dt__gt=appt.start_dt,
    ).exclude(pk=appt.pk).exists()

    if conflict:
        appt.status = Appointment.Status.REJECTED
        appt.save(update_fields=["status"])
        messages.error(request, "Konflikt termina — zahtjev je automatski odbijen.")
        return redirect("staff_requests")

    appt.status = Appointment.Status.APPROVED
    appt.save(update_fields=["status"])
    messages.success(request, "Termin je odobren.")
    return redirect("staff_requests")

@login_required
@staff_required
def staff_reject(request, pk: int):
    staff = StaffProfile.objects.get(user=request.user)
    appt = get_object_or_404(Appointment, pk=pk, staff=staff)

    if request.method != "POST":
        return redirect("staff_requests")

    if appt.status != Appointment.Status.PENDING:
        messages.error(request, "Termin nije u statusu PENDING.")
        return redirect("staff_requests")

    appt.status = Appointment.Status.REJECTED
    appt.save(update_fields=["status"])
    messages.success(request, "Termin je odbijen.")
    return redirect("staff_requests")

@login_required
@staff_required
def staff_mark_done(request, pk: int):
    staff = StaffProfile.objects.get(user=request.user)
    appt = get_object_or_404(Appointment, pk=pk, staff=staff)

    if request.method != "POST":
        return redirect("staff_schedule_today")

    if appt.status != Appointment.Status.APPROVED:
        messages.error(request, "Samo APPROVED termin može biti označen kao DONE.")
        return redirect("staff_schedule_today")

    appt.status = Appointment.Status.DONE
    appt.save(update_fields=["status"])
    messages.success(request, "Termin označen kao DONE.")
    return redirect("staff_schedule_today")
