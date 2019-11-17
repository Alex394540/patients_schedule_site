from django.db import models

from .managers import FreeDayManager


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Settings(SingletonModel):
    
    additional_info = models.TextField(blank=True)


class AppointmentTime(models.Model):

    time = models.DateTimeField()
    
    class Meta:
        ordering = ['time']

    def __str__(self):
    	return "{}:{}".format(str(self.time.hour).rjust(2, '0'), str(self.time.minute).rjust(2, '0'))


class FreeDay(models.Model):

    FREE_DAY_CHOICES = [
        ('Отпуск', 'Отпуск'),
        ('Праздники', 'Праздники'),
        ('Отгул', 'Отгул'),
        ('Без записи', 'Без записи'),
        ('Нерабочая суббота', 'Нерабочая суббота')
    ]

    start = models.DateTimeField()
    end = models.DateTimeField()
    free_day_type = models.CharField(max_length=50, choices=FREE_DAY_CHOICES, default=1)

    objects = FreeDayManager()
    
    class Meta:
        ordering = ['-start', 'end']
        unique_together = ('start', 'end')

    def __str__(self):
        return f"{self.free_day_type} с {self.start} до {self.end}"
