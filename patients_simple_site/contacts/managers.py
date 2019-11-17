from datetime import datetime, date, timedelta
from calendar import Calendar

from django.db import models


class FreeDayManager(models.Manager):

    def fill_saturdays(self, date_from=date.today(), date_to=date.today() + timedelta(days=365)):
        calendar = Calendar()
        cur_date = date_from
        while cur_date < date_to:
            for week in calendar.monthdatescalendar(cur_date.year, cur_date.month):
                # we are interested only in saturdays
                date_ = week[5]
                free_day_type = "Без записи" if date_.day % 2 == 0 else "Нерабочая суббота"
                start = datetime.combine(date_, datetime.min.time())
                end = datetime.combine(date_, datetime.max.time())
                saturdays_in_db = self.model.objects.filter(start__gte=start).filter(end__lte=end)
                if not saturdays_in_db.exists():
                    self.model.objects.create(start=start, end=end, free_day_type=free_day_type)
                else:
                    existing_saturday = saturdays_in_db.first()
                    if existing_saturday.free_day_type not in ('Отпуск', 'Отгул', 'Праздники'):
                        existing_saturday.delete()
                        self.model.objects.create(start=start, end=end, free_day_type=free_day_type)
            cur_date = cur_date.replace(day=28) + timedelta(days=4)
