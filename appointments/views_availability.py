from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvailabilityBlockForm
from .models import AvailabilityBlock, StaffProfile
from .permissions import staff_required

@login_required
@staff_required
def availability_list(request):
    staff = StaffProfile.objects.get(user=request.user)
    blocks = AvailabilityBlock.objects.filter(staff=staff).order_by("date", "start_time")
    return render(request, "availability/list.html", {"blocks": blocks})

@login_required
@staff_required
def availability_create(request):
    staff = StaffProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = AvailabilityBlockForm(request.POST, staff_profile=staff)
        if form.is_valid():
            block = form.save(commit=False)
            block.staff = staff
            block.save()
            messages.success(request, "Dostupnost je dodana.")
            return redirect("availability_list")
    else:
        form = AvailabilityBlockForm(staff_profile=staff)

    return render(request, "availability/form.html", {"form": form, "mode": "create"})

@login_required
@staff_required
def availability_update(request, pk: int):
    staff = StaffProfile.objects.get(user=request.user)
    block = get_object_or_404(AvailabilityBlock, pk=pk, staff=staff)

    if request.method == "POST":
        form = AvailabilityBlockForm(request.POST, instance=block, staff_profile=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Dostupnost je ažurirana.")
            return redirect("availability_list")
    else:
        form = AvailabilityBlockForm(instance=block, staff_profile=staff)

    return render(request, "availability/form.html", {"form": form, "mode": "update", "block": block})

@login_required
@staff_required
def availability_delete(request, pk: int):
    staff = StaffProfile.objects.get(user=request.user)
    block = get_object_or_404(AvailabilityBlock, pk=pk, staff=staff)

    if request.method == "POST":
        block.delete()
        messages.success(request, "Dostupnost je obrisana.")
        return redirect("availability_list")

    return render(request, "availability/confirm_delete.html", {"block": block})
