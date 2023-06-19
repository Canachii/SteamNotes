from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from applist.models import App, Rank
from datetime import datetime
import requests


def update_db(object_list):
    for app in object_list:
        try:
            data = requests.get(f'https://store.steampowered.com/api/appdetails?appids={app.id}&l=korean').json()[
                str(app.id)]
            if data['success'] and data['data']['type'] == 'game' and not data['data']['release_date']['coming_soon']:
                if not data['data']['is_free']:
                    app.initial_price = int(str(data['data']['price_overview']['initial'])[:-2])
                    app.discount_percent = data['data']['price_overview']['discount_percent']
                    app.final_price = int(str(data['data']['price_overview']['final'])[:-2])
                app.name = data['data']['name']
                app.capsule_image = data['data']['capsule_image']
                app.header_image = data['data']['header_image']
                app.is_free = data['data']['is_free']
                app.release_date = datetime.strptime(data['data']['release_date']['date'], '%Y년 %m월 %d일')
                app.save()
            else:
                app.delete()
        except Exception as e:
            print(e)


# Create your views here.
def index(request):
    object_list = App.objects.order_by('?')
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    update_db(page_obj)
    context = {'page_obj': page_obj}
    return render(request, 'index.html', context)


def search(request):
    query = request.GET.get('q')
    object_list = App.objects.filter(
        Q(name__icontains=query) | Q(id__icontains=query)
    )
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    update_db(page_obj)

    context = {'page_obj': page_obj}
    return render(request, 'search.html', context)


def sale(request):
    object_list = App.objects.filter(~Q(discount_percent=0) & Q(discount_percent__isnull=False))
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {'page_obj': page_obj}
    return render(request, 'sale.html', context)


def popular(request):
    object_list = Rank.objects.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    for rank in page_obj:
        try:
            if not rank.app.is_free:
                data = requests.get(f'https://store.steampowered.com/api/appdetails?appids={rank.app_id}&l=korean').json()[
                    str(rank.app_id)]
                if data['success']:
                    if not data['data']['is_free']:
                        rank.app.initial_price = int(str(data['data']['price_overview']['initial'])[:-2])
                        rank.app.discount_percent = data['data']['price_overview']['discount_percent']
                        rank.app.final_price = int(str(data['data']['price_overview']['final'])[:-2])
                    rank.app.name = data['data']['name']
                    rank.app.capsule_image = data['data']['capsule_image']
                    rank.app.header_image = data['data']['header_image']
                    rank.app.is_free = data['data']['is_free']
                    rank.app.release_date = datetime.strptime(data['data']['release_date']['date'], '%Y년 %m월 %d일')
                    rank.app.save()
        except Exception as e:
            print(e)
    context = {'page_obj': page_obj}
    return render(request, 'rank.html', context)


class NextSale(generic.TemplateView):
    template_name = 'next.html'
