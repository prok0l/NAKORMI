from .models import *
from django import forms


class VolunteerCreationForm(forms.ModelForm):

    class Meta:
        model = Volunteer

        fields = (
            'tg_id',
            'name',
            'is_admin',
        )

        widgets = {
            'tg_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
