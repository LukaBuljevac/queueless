from django.conf import settings
from django.db import models
from appointments.models import Appointment

class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review {self.rating}/5 for appt {self.appointment_id}"
