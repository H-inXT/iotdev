from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=15)
    # 用户
    pro_user = models.ForeignKey(User,  on_delete=models.CASCADE)
    # 产品行业
    industry = models.CharField(max_length=30)
    # 产品简介
    industry = models.CharField(max_length=50)
    internet_connect = models.CharField(max_length=20, default="移动蜂窝网络")
    protocol = models.CharField(max_length=20, default="MQTT")
    system = models.CharField(max_length=20, default="无")
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.product_name

class Device(models.Model):
    device_name = models.CharField(max_length=30)
    pro_user = models.ForeignKey(User,  on_delete=models.CASCADE)
    # 关联产品
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # 鉴权
    authentication = models.CharField(max_length=50)
    # 描述
    describe = models.CharField(max_length=150)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    # def get_url(self):
        # return comment.text + '\n' + reverse('blog_detail', kwargs={'blog_pk': self.pk})

    # def get_email(self):
    #     return self.author.email

    def __str__(self):
        return "<Device: %s>" % self.device_name

    class Meta:
        ordering = ['-created_time'] # '-'号是倒叙

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    time = models.DateTimeField()