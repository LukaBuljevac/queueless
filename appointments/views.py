from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

def _require_role(request, role: str):
    u = request.user
    if getattr(u, "is_superuser", False):
        return None
    if getattr(u, "role", None) != role:
        return HttpResponseForbidden("403 Forbidden")
    return None

@login_required
def client_dashboard(request):
    denied = _require_role(request, "CLIENT")
    if denied: return denied
    return render(request, "dash/client.html")

@login_required
def staff_dashboard(request):
    denied = _require_role(request, "STAFF")
    if denied: return denied
    return render(request, "dash/staff.html")

@login_required
def admin_dashboard(request):
    u = request.user
    if not (getattr(u, "is_superuser", False) or u.role == "ADMIN"):
        return HttpResponseForbidden("403 Forbidden")
    return render(request, "dash/admin.html")
