from django.forms import ModelForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Appointment
from datetime import timedelta


class AppointmentForm(ModelForm):
    
    class Meta:
        model = Appointment
        fields = ['time', 'comment', 'created_session']

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        appointment_time = cleaned_data['time']
        if appointment_time >= timezone.now() + timedelta(days=365):
            raise ValidationError('Выберите дату пораньше')
        return cleaned_data
