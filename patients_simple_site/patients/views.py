from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import Appointment, FreeDay
from .forms import AppointmentForm


def show_day(request, year, month, day):
    appointments = Appointment.objects.days_appointments(year, month, day)
    return render(request, 'patients/show_day.html', {'appointments': appointments})


def show_week(request, year, month, day):
    
    # Create new session if has not been created
    if not request.session.session_key:
        request.session.create()

    appointments = Appointment.objects.get_week_appointments_for_display(year, month, day)
    monday, tuesday, wednesday, thursday, friday = Appointment.get_weekdays_dates(year, month, day)
    weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',)
    
    # Change data depending from user
    free_day_types = [free_day['free_day_type'] for free_day in FreeDay.objects.values('free_day_type')]
    if not request.user.is_superuser:
        for dictionary in appointments:

            # compare date with current
            for date_, weekday in zip((monday, tuesday, wednesday, thursday, friday), weekdays):
                hour, minute = map(int, dictionary['time'].split(':'))
                datetime_ = datetime(date_.year, date_.month, date_.day, hour, minute)
                dictionary[f"{weekday}_not_available"] = datetime_ <= datetime.now()
                dictionary[f"{weekday}_set_in_session"] = None

            for weekday in weekdays:
                if dictionary[weekday] and dictionary[weekday] not in free_day_types:
                    dictionary[f"{weekday}_set_in_session"] = dictionary[weekday].created_session
                    dictionary[weekday] = 'Занято'

    prev_week_start_url = Appointment.get_prev_week_url(year, month, day)
    next_week_start_url = Appointment.get_next_week_url(year, month, day)
    return render(request, 'patients/show_calendar.html', 
        {'appointments': appointments,
         'monday': monday.strftime('%Y-%m-%d'),
         'tuesday': tuesday.strftime('%Y-%m-%d'),
         'wednesday': wednesday.strftime('%Y-%m-%d'),
         'thursday': thursday.strftime('%Y-%m-%d'),
         'friday': friday.strftime('%Y-%m-%d'),
         'prev_week_url': prev_week_start_url,
         'next_week_url': next_week_start_url
        })


def show_calendar(request):
    week_start = Appointment.count_start_of_week()
    return show_week(request, week_start.year, week_start.month, week_start.day)


@require_http_methods(["POST"])
def add_appointment(request):

    date_ = request.POST['date']
    time_ = request.POST['time']
    comment = request.POST['comment']
    session_key = request.session.session_key
    if not session_key:
        return HttpResponse(status=400)

    # check if there was appointment with this session
    appointment = Appointment.objects.filter(time__gte=datetime.now(), created_session=session_key)
    if appointment.exists():
        return HttpResponse(status=405)
    
    datetime_string = date_ + ' ' + time_
    appointment_datetime = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
    form = AppointmentForm({'comment': comment, 'time': appointment_datetime, 'created_session': session_key})
    if form.is_valid():
        appointment = form.save()
        request.session.set_expiry(int((appointment_datetime - datetime.now()).total_seconds()))
        return HttpResponse('OK')
    else:
        return HttpResponse(status=400)


@require_http_methods(["POST"])
def remove_appointment(request):

    date_ = request.POST['date']
    time_ = request.POST['time']
    session_key = request.session.session_key
    if not session_key:
        return HttpResponse(status=400)
    
    datetime_string = date_ + ' ' + time_
    appointment_datetime = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')

    appointment = Appointment.objects.filter(time=appointment_datetime, created_session=session_key)
    if appointment.exists():
        appointment.delete()
        return HttpResponse('OK')
    else:
        return HttpResponse(status=400)