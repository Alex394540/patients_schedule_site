# Generated by Django 2.2.5 on 2019-10-03 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_freeday_free_day_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FreeDay',
        ),
    ]
