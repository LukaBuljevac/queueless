from django.urls import path
from .views import client_dashboard, staff_dashboard, admin_dashboard
from .views_availability import (
    availability_list, availability_create, availability_update, availability_delete
)
from .views_booking import book_appointment
from .views_client import my_appointments, cancel_appointment
from .views_staff_appointments import (
    staff_requests, staff_schedule_today, staff_approve, staff_reject, staff_mark_done
)


urlpatterns = [
    # CLIENT
    path("client/", client_dashboard, name="client_dashboard"),
    path("client/book/", book_appointment, name="book_appointment"),
    path("client/my/", my_appointments, name="my_appointments"),
    path("client/my/<int:pk>/cancel/", cancel_appointment, name="cancel_appointment"),

    # STAFF
    path("staff/", staff_dashboard, name="staff_dashboard"),
    path("staff/availability/", availability_list, name="availability_list"),
    path("staff/availability/new/", availability_create, name="availability_create"),
    path("staff/availability/<int:pk>/edit/", availability_update, name="availability_update"),
    path("staff/availability/<int:pk>/delete/", availability_delete, name="availability_delete"),

    path("staff/requests/", staff_requests, name="staff_requests"),
    path("staff/requests/<int:pk>/approve/", staff_approve, name="staff_approve"),
    path("staff/requests/<int:pk>/reject/", staff_reject, name="staff_reject"),
    path("staff/today/", staff_schedule_today, name="staff_today"),
    path("staff/today/<int:pk>/done/", staff_mark_done, name="staff_mark_done"),

    # ADMIN
    path("admin/", admin_dashboard, name="admin_dashboard"),
]

