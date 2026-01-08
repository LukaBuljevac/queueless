from django.http import HttpResponseForbidden
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        u = request.user
        if not u.is_authenticated:
            return HttpResponseForbidden("403 Forbidden")
        if getattr(u, "is_superuser", False) or getattr(u, "role", None) == "STAFF":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("403 Forbidden")
    return _wrapped
