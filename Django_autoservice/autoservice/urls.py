from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobilis/<int:car_id>/', views.automobilis_detail, name='automobilis_detail'),
    path('uzsakymai/', views.OrderListView.as_view(), name='uzsakymai'),
    path('uzsakymas/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('search/', views.search, name='search'),
    path('mano_uzsakymai/', views.KlientoUzsakymuSarasas.as_view(), name='mano-uzsakymai'),
    path('register/', views.register, name='register'),
    path('uzsakymas/<uuid:order_id>/', views.order_detail, name='order-detail'),
    path('profilis/', views.profilis, name='profilis'),

]


