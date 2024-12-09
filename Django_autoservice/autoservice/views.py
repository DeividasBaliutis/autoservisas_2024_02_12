from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import CarModel, Car, Service, Order, OrderLine, Profilis
from django.views import View, generic
from django.db.models import Q
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import OrderReviewForm, UserUpdateForm, ProfilisUpdateForm
from django.views.generic.edit import FormMixin


# Pagrindinis puslapis
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

    return render(request, 'index.html', context=context)


# Automobilių sąrašas su puslapiavimu
def automobiliai(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    automobiliai = paginator.get_page(page_number)

    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'automobiliai.html', context=context)


# Automobilių detalus
def automobilis_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car
    }
    return render(request, 'automobilis_detail.html', context)


# Užsakymų sąrašas su puslapiavimu
class OrderListView(View):
    def get(self, request):
        paginator = Paginator(Order.objects.all(), 3)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        context = {
            'orders': orders
        }

        return render(request, 'uzsakymai.html', context)


# Užsakymo detalus
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_lines = OrderLine.objects.filter(order=order)
    form = OrderReviewForm(initial={'order': order, 'reviewer': request.user})
    reviews = order.orderreview_set.all()

    if request.method == "POST":
        form = OrderReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Atsiliepimas sėkmingai pridėtas!')
            return redirect('order-detail', order_id=order.id)

    context = {
        'order': order,
        'order_lines': order_lines,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'order_detail.html', context)


# Paieška
def search(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(license_plate__icontains=query) |
        Q(vin__icontains=query) |
        Q(customer__icontains=query) |
        Q(car_model__make__icontains=query) |
        Q(car_model__model__icontains=query)
    )
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})


# Kliento užsakymų sąrašas
class KlientoUzsakymuSarasas(FormMixin, LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'vartotojo_uzsakymai.html'
    paginate_by = 10
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-date')


# Registracijos funkcionalumas
@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                return redirect('register')
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.info(request, f'Vartotojas {username} užregistruotas!')
                return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


# Profilio atnaujinimas
from django.contrib.auth.decorators import login_required


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)
