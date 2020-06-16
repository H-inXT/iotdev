
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('bind_email_code/', views.send_verification_code, name='send_verification_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reg_product/', views.reg_product, name='reg_product'),
    # path('reg_device/', views.reg_device, name='reg_device'),
    # path('regproduct/', views.regproduct, name='regproduct'),
    # send_verification_code

]

# 设置一个路径指向到哪个位置
# urlpatterns += static('/media/', document_root=settings.MEDOA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
