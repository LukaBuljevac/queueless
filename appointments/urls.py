from django.urls import path
from .views import client_dashboard, staff_dashboard, admin_dashboard
from .views_availability import (
    availability_list, availability_create, availability_update, availability_delete
)
from .views_booking import book_appointment
from .views_client import my_appointments

urlpatterns = [
    # CLIENT
    path("client/", client_dashboard, name="client_dashboard"),
    path("client/book/", book_appointment, name="book_appointment"),
    path("client/my/", my_appointments, name="my_appointments"),

    # STAFF
    path("staff/", staff_dashboard, name="staff_dashboard"),
    path("staff/availability/", availability_list, name="availability_list"),
    path("staff/availability/new/", availability_create, name="availability_create"),
    path("staff/availability/<int:pk>/edit/", availability_update, name="availability_update"),
    path("staff/availability/<int:pk>/delete/", availability_delete, name="availability_delete"),

    # ADMIN
    path("admin/", admin_dashboard, name="admin_dashboard"),
]
