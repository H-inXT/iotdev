from django.contrib import admin
from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # http://localhostL8000/blog
    path('', views.product_list, name='product_list'),
    path('<int:dev_pk>/', views.device_list, name='device_list'),
    path('is_online/', views.is_online, name='is_online'),
    path('reg_device/', views.reg_device, name='reg_device'),
    path('internet/<str:name>', views.product_internet, name='product_internet'),
    path('history/<int:dev_pk>', views.history, name='history'),
    path('deleteDevice/<int:id>/<int:dev_pk>', views.delete_device, name='delete_device'),
    path('deleteProduct/<int:id>/', views.delete_product, name='delete_product'),
    path('date/<int:year>/<int:month>/', views.pros_with_date, name='pros_with_date'),
    path('datewithdevs/<int:year>/<int:month>/', views.devs_with_date, name='devs_with_date'),
    path('dataswithdate/<int:year>/<int:month>/', views.datas_with_date, name='datas_with_date'),
]
