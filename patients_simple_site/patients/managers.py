from datetime import datetime, timedelta, date

from django.db import models

from contacts.models import AppointmentTime, FreeDay


class AppointmentManager(models.Manager):
    
    def days_appointments(self, year, month, day):
        appointments = self.model.objects.filter(time__gte=datetime(year, month, day), time__lte=datetime(year, month, day, 23, 59, 59))
        return appointments

    def week_appointments(self, year, month, day):
        start_of_week = self.model.count_start_of_week(datetime(year, month, day))
        end_of_week = start_of_week + timedelta(days=6)
        appointments = self.model.objects.filter(time__gte=datetime(start_of_week.year, start_of_week.month, start_of_week.day), 
                                                 time__lte=datetime(end_of_week.year, end_of_week.month, end_of_week.day, 23, 59, 59))
        return appointments

    def get_week_appointments_for_display(self, year, month, day):
        appointment_times = AppointmentTime.objects.all()
        free_days = list(FreeDay.objects.all())
        monday_date, tuesday_date, wednesday_date, thursday_date, friday_date = self.model.get_weekdays_dates(year, month, day)

        # Fill info about free days
        common_dates_dict = {}
        for t in appointment_times:
            common_dates_dict[t.time.hour, t.time.minute] = {monday_date: '', tuesday_date: '', 
                                                             wednesday_date: '', thursday_date: '', 
                                                             friday_date: ''}
            
            for date_ in (monday_date, tuesday_date, wednesday_date, thursday_date, friday_date,):
                dt = datetime(date_.year, date_.month, date_.day, t.time.hour, t.time.minute)
                for free_day in free_days:
                    if free_day.start <= dt <= free_day.end:
                        common_dates_dict[t.time.hour, t.time.minute][date_] = free_day.free_day_type
        
        # Fill also data about appointments
        appointments = self.week_appointments(year, month, day)
        for appointment in appointments:
            dt = appointment.time
            common_dates_dict[dt.hour, dt.minute][dt.date()] = common_dates_dict[dt.hour, dt.minute][dt.date()] or appointment
        
        # Transform into list and sort...
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        data_for_display = []
        for time, events in common_dates_dict.items():
            prepared_for_display_dict = {weekdays[d.weekday()]: common_dates_dict[time][d] for d in events.keys()}
            prepared_for_display_dict['time'] = str(time[0]).rjust(2, '0') + ':' + str(time[1]).rjust(2, '0')
            data_for_display.append(prepared_for_display_dict)

        data_for_display.sort(key=lambda x: x['time'])
        return data_for_display
