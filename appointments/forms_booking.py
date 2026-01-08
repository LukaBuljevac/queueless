from django import forms
from services.models import Service
from .models import StaffProfile

class BookingSearchForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    staff = forms.ModelChoiceField(
        queryset=StaffProfile.objects.all(),  # default
        widget=forms.Select(attrs={"class": "form-control"})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ako je service odabran, filtriraj staff koji nudi tu uslugu
        service_id = None
        if self.is_bound:
            service_id = self.data.get("service")

        if service_id:
            self.fields["staff"].queryset = StaffProfile.objects.filter(
                staff_services__service_id=service_id
            ).distinct()
