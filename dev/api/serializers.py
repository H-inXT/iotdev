from rest_framework import serializers
from ..models import Product, Device, Data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product   # 要序列化的模型
        fields = '__all__'   # 要序列化的字段

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'
