from django.shortcuts import render

from .models import Settings


def show_contacts(request):
    settings = Settings.load()
    return render(request, 'contacts/contacts.html', {'data': settings})
