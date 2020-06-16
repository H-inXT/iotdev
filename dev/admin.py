from django.contrib import admin
from .models import Product, Device, Data

# Register your models here.
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'pro_user', 'internet_connect', 'protocol','internet_connect','system', 'created_time')

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_name', 'product', 'pro_user', 'created_time', 'last_updated_time')

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'value', 'time')
