import string
import random
import datetime
import time
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse # 反向解析
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm, RegProductForm
from .models import Profile
from dev.models import Product

def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        request.session['username'] = user.username
        request.session['user_id'] = user.id
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            if user is not None:
                auth.login(request, user) # 登录到后台的用户
                #                               获取from=后面的内容
                # user = User.objects.get(username=username)
                # request.session['user_id'] = user.id
                return redirect(request.GET.get('from', reverse('home')))# 跳转到刚才登录的页面
            else:
                login_form.add_error(None, '用户名或密码不正确')
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password) # 方法一
            user.save()
            
            # 清除session
            del request.session['register_code']

            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

            # user = User()  # 方法二
            # user.username = username
            # user.email = email
            # user.set_password(password)
            # user.save()
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def logout(request):
    auth.logout(request)
    context = {}
    return redirect(request.GET.get('from', reverse('home')))
    # return reverse('home')
    # return render(request, 'home.html', context)

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    redirect_to = redirect(request.GET.get('from', reverse('home')))
    # redirect_to = reverse('home')

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = redirect(request.GET.get('from', reverse('home')))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码 由列表变为字符串 ''.join()
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
        
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                '1280128507@qq.com',
                [email],
                fail_silently=False
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    redirect_to = reverse('home')

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)

            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def forgot_password(request):
    redirect_to = reverse('login')

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)

def reg_product(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = RegProductForm(request.POST, user=request.user)
        if form.is_valid():
            # user = request.user
            product_name = form.cleaned_data['product_name']
            internet_connect = form.cleaned_data['internet_connect']
            protocol = form.cleaned_data['protocol']
            system = form.cleaned_data['system']
            industry = form.cleaned_data['industry']

            product = Product()
            product.product_name = product_name
            product.industry = industry
            product.internet_connect = internet_connect
            product.protocol = protocol
            product.system = system
            product.pro_user = request.user
            product.save()

            return redirect(redirect_to)
    else:
        form = RegProductForm()

    context = {}
    context['page_title'] = '注册产品'
    context['form_title'] = '注册产品'
    context['submit_text'] = '注册'
    context['form'] = form
    # context = {}
    # context['reg_form'] = reg_form
    return render(request, 'form.html', context)

