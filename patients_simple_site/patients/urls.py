from django.urls import path
from . import views

app_name = 'patients'
urlpatterns = [
    path('calendar/', views.show_calendar, name='calendar'),
    path('day/<int:year>/<int:month>/<int:day>/', views.show_day),
    path('week/<int:year>/<int:month>/<int:day>/', views.show_week),
    path('add_appointment/', views.add_appointment),
    path('remove_appointment/', views.remove_appointment)
]