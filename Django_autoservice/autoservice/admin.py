from django.contrib import admin
from .models import CarModel, Car, Service, Order, OrderLine, OrderReview, Profilis


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'car', 'status', 'customer', 'return_date', 'description')
    inlines = [OrderLineInline]
    list_editable = ('status',)


class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vin', 'customer', 'car_model', 'description')
    list_filter = ('customer', 'car_model')
    search_fields = ('license_plate', 'vin')


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')


admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Service)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(Profilis)