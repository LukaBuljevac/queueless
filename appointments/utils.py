from datetime import datetime, timedelta
from typing import List, Tuple
from django.utils import timezone

from .models import AvailabilityBlock, Appointment

SLOT_MINUTES = 30

def generate_slots(staff, service, date) -> List[Tuple[datetime, datetime]]:
    slots = []

    blocks = AvailabilityBlock.objects.filter(staff=staff, date=date)
    duration = timedelta(minutes=service.duration_min)

    tz = timezone.get_current_timezone()

    # Učitaj termine koji blokiraju slotove
    appointments = Appointment.objects.filter(
        staff=staff,
        start_dt__date=date,
        status__in=[Appointment.Status.PENDING, Appointment.Status.APPROVED],
    )

    for block in blocks:
        start_naive = datetime.combine(date, block.start_time)
        end_naive = datetime.combine(date, block.end_time)

        start = timezone.make_aware(start_naive, tz)
        end = timezone.make_aware(end_naive, tz)

        current = start
        while current + duration <= end:
            slot_end = current + duration

            conflict = appointments.filter(
                start_dt__lt=slot_end,
                end_dt__gt=current
            ).exists()

            if not conflict:
                slots.append((current, slot_end))

            current += timedelta(minutes=SLOT_MINUTES)

    return slots
