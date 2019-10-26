from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import News


def show_news(request):
    all_news = News.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_news, 4)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'news/show_news.html', {'news': news})


def read_item(request, pk):
    try:
        item = News.objects.get(pk=pk)
    except ObjectDoesNotExists:
        raise Http404('Новость не найдена!')
    return render(request, 'news/read_news.html', {'item': item})
