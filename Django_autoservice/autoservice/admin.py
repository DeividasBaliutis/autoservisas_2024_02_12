from django.contrib import admin
from .models import CarModel, Car, Service, Order, OrderLine

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'car' , 'status')
    inlines = [OrderLineInline]
    list_editable = ('status',)

class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vin','customer','car_model')
    list_filter = ('customer', 'car_model')
    search_fields = ('license_plate', 'vin')



admin.site.register(CarModel)
admin.site.register(Car , CarAdmin)
admin.site.register(Service)
admin.site.register(Order , OrderAdmin)
admin.site.register(OrderLine)




