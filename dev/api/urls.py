from django.urls import path
from . import views

app_name = 'dev'   # 指定命名空间

urlpatterns = [
    path('Products/', views.ProductList.as_view(), name='Product_list'),
    path('Products/<pk>/', views.ProductDetail.as_view(), name='Product_detail'),
    path('Devices/', views.DeviceList.as_view(), name='Device_list'),
    path('Devices/<pk>/', views.DeviceDetail.as_view(), name='Device_detail'),
    path('Datas/', views.DataList.as_view(), name='Data_list'),
    path('Datas/<pk>/', views.DataDetail.as_view(), name='Data_detail'),
]