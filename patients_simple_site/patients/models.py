import logging
from datetime import timedelta, date, datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .managers import AppointmentManager
from contacts.models import FreeDay


log = logging.getLogger('appointments')


class Appointment(models.Model):

    time = models.DateTimeField()
    comment = models.CharField(max_length=150)
    created_session = models.TextField()
    
    objects = AppointmentManager()
    
    class Meta:
        ordering = ['-time']

    @classmethod
    def extract_day_url(cls, dt):
        return f"{dt.year}/{dt.month}/{dt.day}/"

    @classmethod
    def count_start_of_week(cls, dt=datetime.now()):
        weekday = dt.weekday()
        if weekday in (5,6):
            return dt + timedelta(days=7-weekday)
        return dt - timedelta(days=weekday)

    @classmethod
    def get_weekdays_dates(cls, year, month, day):
        return [date(year, month, day) + timedelta(days=i) for i in range(5)]

    @classmethod
    def get_prev_week_start(cls, dt):
        start_of_week = cls.count_start_of_week(dt)
        return start_of_week - timedelta(days=7)

    @classmethod
    def get_next_week_start(cls, dt):
        start_of_week = cls.count_start_of_week(dt)
        return start_of_week + timedelta(days=7)

    @classmethod
    def get_prev_week_url(cls, year, month, day):
        dt = date(year, month, day)
        return cls.extract_day_url(cls.get_prev_week_start(dt))

    @classmethod
    def get_next_week_url(cls, year, month, day):
        dt = date(year, month, day)
        return cls.extract_day_url(cls.get_next_week_start(dt))

    def save(self, *args, **kwargs):
        if self.is_valid():
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Выбрано нерабочее время! Попробуйте еще раз')

    def is_valid(self):
        freedays = FreeDay.objects.filter(start__gte=self.time, end__lte=self.time)
        return self.time.weekday() not in (5,6) and not freedays.exists()

    def get_absolute_url(self):
        return f"appointment/{self.pk}/"

    def __str__(self):
        return f"Запись на {self.time}. \n{self.comment}."


@receiver(pre_save, sender=Appointment)
def appointment_creation_audit(sender, instance, **kwargs):
    log.info("Запланировано обследование: " + str(instance))


@receiver(pre_delete, sender=Appointment)
def appointment_deletion_audit(sender, instance, **kwargs):
    log.info("Удалено обследование: " + str(instance))

