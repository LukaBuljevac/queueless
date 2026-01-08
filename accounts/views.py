from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

def landing(request):
    return render(request, "landing.html")

@login_required
def role_home(request):
    u = request.user
    if getattr(u, "is_superuser", False) or u.role == "ADMIN":
        return redirect("admin_dashboard")
    if u.role == "STAFF":
        return redirect("staff_dashboard")
    return redirect("client_dashboard")
