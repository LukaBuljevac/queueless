from datetime import timedelta
from django.utils import timezone

CANCEL_MIN_HOURS = 24

def can_client_cancel(appointment) -> bool:
    """
    Client smije otkazati samo ako je termin PENDING ili APPROVED
    i ako je do termina ostalo >= CANCEL_MIN_HOURS.
    """
    if appointment.status not in [appointment.Status.PENDING, appointment.Status.APPROVED]:
        return False
    now = timezone.now()
    return appointment.start_dt - now >= timedelta(hours=CANCEL_MIN_HOURS)
