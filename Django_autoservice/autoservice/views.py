from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import CarModel, Car, Service, Order, OrderLine
from django.views import View
from django.db.models import Q


def index(request):
    sum_services = Service.objects.all().count()
    cars = Car.objects.count()
    sum_order = Order.objects.filter(status='COMPLETED').count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'sum_cars': cars,
        'services': sum_services,
        'sum_order': sum_order,
        'num_visits': num_visits
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)


def automobiliai(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    automobiliai = paginator.get_page(page_number)

    # automobiliai = Car.objects.all()
    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'automobiliai.html', context=context)


def automobilis_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car
    }
    return render(request, 'automobilis_detail.html', context)


class OrderListView(View):
    def get(self, request):
        paginator = Paginator(Order.objects.all(), 3)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        context = {
            'orders': orders
        }

        return render(request, 'uzsakymai.html', context)


def order_detail(request, order_id):
    # Gauti užsakymą pagal jo ID
    order = get_object_or_404(Order, id=order_id)

    # Gauti susijusias užsakymo eilutes
    order_lines = OrderLine.objects.filter(order=order)

    # Sukurti kontekstą su užsakymo ir eilučių informacija
    context = {
        'order': order,
        'order_lines': order_lines
    }

    return render(request, 'order_detail.html', context)


def search(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(license_plate__icontains=query) |
        Q(vin__icontains=query) |
        Q(customer__icontains=query) |
        Q(car_model__make__icontains=query) |
        Q(car_model__model__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})
