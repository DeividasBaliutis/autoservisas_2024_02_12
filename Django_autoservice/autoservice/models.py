from django.db import models
import uuid


class CarModel(models.Model):
    make = models.CharField('Marke', max_length=100, help_text='Įveskite automobilio markę')
    model = models.CharField('Modelis', max_length=100, help_text='Įveskite automobilio modelį')

    class Meta:
        verbose_name = 'AutoModelis'
        verbose_name_plural = 'AutoModeliai'


    def __str__(self):
        return f'{self.make} {self.model}'


class Car(models.Model):
    license_plate = models.CharField('Valstybinis numeris', max_length=20, help_text='Įveskite automobilio valstybinį numerį')
    vin = models.CharField('VIN kodas', max_length=50, help_text='Įveskite automobilio VIN kodą')
    customer = models.CharField('Kleintas', max_length=100, help_text='Įveskite kliento vardą arba pavadinimą')
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, help_text='Pasirinkite automobilio modelį')

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

    def __str__(self):
        return f'{self.license_plate} ({self.car_model})'


class Service(models.Model):
    name = models.CharField('Paslauga', max_length=100, help_text='Įveskite paslaugos pavadinimą (pvz., Alyvos keitimas)')
    price = models.DecimalField('Kaina', max_digits=10, decimal_places=2, help_text='Įveskite paslaugos kainą (pvz., 50.00)')

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'

    def __str__(self):
        return f'{self.name} ({self.price} EUR)'


class Order(models.Model):

    STATUS_CHOICES = [
        ('NEW', 'Naujas'),
        ('IN_PROGRESS', 'Vykdomas'),
        ('COMPLETED', 'Užbaigtas'),
        ('CANCELLED', 'Atšauktas'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus užsakymo ID')
    date = models.DateTimeField('Data', help_text='Įveskite užsakymo datą')
    car = models.ForeignKey( Car, on_delete=models.SET_NULL, null=True, help_text='Pasirinkite automobilį, kuriam skirtas užsakymas')
    status = models.CharField(
        'Statusas',
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        help_text='Pasirinkite užsakymo būseną'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Uzsakymas'
        verbose_name_plural = 'Uzsakymai'


    def __str__(self):
        return f'Uzsakymas {self.id}'


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True , help_text='Pasirinkite užsakymą, kuriam priskirta eilutė')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, help_text='Pasirinkite atliktą paslaugą')
    quantity = models.PositiveIntegerField('Kiekis', help_text='Įveskite atliktų paslaugų kiekį')

    class Meta:
        verbose_name = 'UzsakymoEilute'
        verbose_name_plural = 'UzsakymoEilutes'

    def __str__(self):
        return f'{self.order} - {self.service} ({self.quantity} vnt.)'
