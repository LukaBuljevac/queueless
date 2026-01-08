from datetime import datetime, timedelta
from typing import List
from .models import AvailabilityBlock, Appointment

SLOT_MINUTES = 30

def generate_slots(staff, service, date) -> List[tuple]:
    """
    Vraća listu (start_dt, end_dt) slobodnih slotova
    """
    slots = []

    blocks = AvailabilityBlock.objects.filter(staff=staff, date=date)
    appointments = Appointment.objects.filter(
        staff=staff,
        start_dt__date=date,
        status__in=["PENDING", "APPROVED"]
    )

    duration = timedelta(minutes=service.duration_min)

    for block in blocks:
        start = datetime.combine(date, block.start_time)
        end = datetime.combine(date, block.end_time)

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
