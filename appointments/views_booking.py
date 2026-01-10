from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms_booking import BookingSearchForm
from .models import Appointment
from .utils import generate_slots


@login_required
def book_appointment(request):
    # autorizacija
    if request.user.role != "CLIENT":
        return render(request, "403.html", status=403)

    form = BookingSearchForm(request.GET or None)
    slots = []

    if form.is_valid():
        service = form.cleaned_data["service"]
        staff = form.cleaned_data["staff"]
        date = form.cleaned_data["date"]

        # prikaz dostupnih slotova
        slots = generate_slots(staff, service, date)

        # rezervacija odabranog slota
        if request.method == "POST":
            start_iso = request.POST.get("start")
            end_iso = request.POST.get("end")

            if not start_iso or not end_iso:
                messages.error(request, "Neispravan zahtjev. Odaberi termin ponovno.")
                return redirect(f"{request.path}?{request.META.get('QUERY_STRING','')}")

            try:
                start_dt = datetime.fromisoformat(start_iso)
                end_dt = datetime.fromisoformat(end_iso)
            except ValueError:
                messages.error(request, "Neispravan format datuma/vremena.")
                return redirect(f"{request.path}?{request.META.get('QUERY_STRING','')}")

            tz = timezone.get_current_timezone()

            # fromisoformat može vratiti naive ili aware — pokrij oba slučaja
            if timezone.is_naive(start_dt):
                start_dt = timezone.make_aware(start_dt, tz)
            else:
                start_dt = start_dt.astimezone(tz)

            if timezone.is_naive(end_dt):
                end_dt = timezone.make_aware(end_dt, tz)
            else:
                end_dt = end_dt.astimezone(tz)

            # ne dopusti rezervaciju u prošlosti
            if start_dt < timezone.now():
                messages.error(request, "Ne možeš rezervirati termin u prošlosti.")
                return redirect(f"{request.path}?{request.META.get('QUERY_STRING','')}")

            # double-booking zaštita (server-side)
            conflict = Appointment.objects.filter(
                staff=staff,
                status__in=[Appointment.Status.PENDING, Appointment.Status.APPROVED],
                start_dt__lt=end_dt,
                end_dt__gt=start_dt,
            ).exists()

            if conflict:
                messages.error(request, "Nažalost, taj termin je upravo zauzet. Osvježi i odaberi drugi.")
                return redirect(f"{request.path}?{request.META.get('QUERY_STRING','')}")

            Appointment.objects.create(
                client=request.user,
                staff=staff,
                service=service,
                start_dt=start_dt,
                end_dt=end_dt,
                status=Appointment.Status.PENDING,
            )

            messages.success(request, "Termin je rezerviran (na čekanju potvrde).")
            return redirect("my_appointments")

    return render(request, "booking/book.html", {"form": form, "slots": slots})
