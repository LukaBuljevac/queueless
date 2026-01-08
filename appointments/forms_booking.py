from django import forms
from services.models import Service
from .models import StaffProfile

class BookingSearchForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    staff = forms.ModelChoiceField(
        queryset=StaffProfile.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
