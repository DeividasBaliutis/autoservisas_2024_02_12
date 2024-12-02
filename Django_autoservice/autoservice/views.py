from itertools import count
from django.shortcuts import render , get_object_or_404
from .models import CarModel, Car, Service, Order , OrderLine
from django.views import View


def index(request):
    # Suskaičiuokime keletą pagrindinių objektų
    sum_services = Service.objects.all().count()
    cars = Car.objects.count()
    sum_order = sum_order = Order.objects.filter(status='COMPLETED').count()


    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'sum_cars': cars,
        'services': sum_services,
        'sum_order': sum_order,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)


def automobiliai(request):
    automobiliai = Car.objects.all()
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
        # Paimame visus užsakymus
        orders = Order.objects.all()

        # Perduodame užsakymus į šabloną
        context = {
            'orders': orders
        }

        # Atvaizduojame šabloną
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

    # Grąžinti užsakymo detalių šabloną su duomenimis
    return render(request, 'order_detail.html', context)