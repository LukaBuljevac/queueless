from django.contrib import admin
from .models import StaffProfile, StaffService, AvailabilityBlock, Appointment

admin.site.register(StaffProfile)
admin.site.register(StaffService)
admin.site.register(AvailabilityBlock)
admin.site.register(Appointment)
