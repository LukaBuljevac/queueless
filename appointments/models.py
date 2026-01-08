from django.conf import settings
from django.db import models
from services.models import Service

class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Staff: {self.user.username}"

class StaffService(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="staff_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("staff", "service")

class AvailabilityBlock(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="availability")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["date", "start_time"]

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CANCELLED = "CANCELLED", "Cancelled"
        DONE = "DONE", "Done"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments")
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField()

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_dt"]
        indexes = [
            models.Index(fields=["staff", "start_dt"]),
            models.Index(fields=["client", "start_dt"]),
        ]
