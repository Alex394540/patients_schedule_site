from datetime import datetime, date, timedelta

from django.test import TestCase
from django.urls import reverse
from contacts.models import AppointmentTime
from .models import Appointment


# Create your tests here.
class TestSchedule(TestCase):

    def test_basic_schedule_displaying(self):
        response = self.client.get(reverse('patients:calendar'))
        self.assertEquals(response.status_code, 200)
    
    def test_filled_schedule_displaying(self):
        
        # at least several will be weekdays
        base_dates = [date.today() + timedelta(days=i) for i in range(5)]
        times = [(9, 20), (10, 0), (11, 0), (12, 15), (14, 30)]
        AppointmentTime.objects.bulk_create([AppointmentTime(time=datetime(year=date_.year, month=date_.month, day=date_.day,
                                                                           hour=hour_, minute=minute_))
                for hour_, minute_ in times
                for date_ in base_dates
            ])

        appointment_times = AppointmentTime.objects.all()
        appointments = Appointment.objects.bulk_create([
                Appointment(time=time.time, comment='Comment' + str(ind), created_session='Session' + str(ind)) 
                for ind, time in enumerate(appointment_times)
            ])

        response = self.client.get(reverse('patients:calendar'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Занято')
