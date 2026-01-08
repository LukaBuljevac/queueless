from django import forms
from .models import AvailabilityBlock

class AvailabilityBlockForm(forms.ModelForm):
    class Meta:
        model = AvailabilityBlock
        fields = ["date", "start_time", "end_time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

    def __init__(self, *args, staff_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.staff_profile = staff_profile

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("date")
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")

        if date and start and end:
            if end <= start:
                raise forms.ValidationError("Vrijeme završetka mora biti nakon vremena početka.")

            qs = AvailabilityBlock.objects.filter(staff=self.staff_profile, date=date)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            overlaps = qs.filter(start_time__lt=end, end_time__gt=start).exists()
            if overlaps:
                raise forms.ValidationError("Ovaj blok se preklapa s postojećom dostupnošću.")

        return cleaned
