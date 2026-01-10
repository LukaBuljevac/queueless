from django.contrib import admin
from .models import Appointment, StaffProfile, AvailabilityBlock

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("start_dt", "client", "staff", "service", "status")
    list_filter = ("status", "staff")
    search_fields = ("client__username", "staff__user__username")

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    list_display = ("staff", "date", "start_time", "end_time")
