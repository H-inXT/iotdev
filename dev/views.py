import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Device, Data
from django.conf import settings
from django.db.models import Count
from django.core.paginator import Paginator

# Create your views here.

def get_blog_list_common_data(request, pros_all_list):
    paginator = Paginator(pros_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每each_pageblogs_number篇进行分页
    page_num = request.GET.get('page', 1)# 获取页面参数（GET请求）
    page_of_s = paginator.get_page(page_num)
    currentr_page_num = page_of_s.number# 获取当前页码
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))# 后面的是+2+1取开区间的最大值
    # 加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页的按钮页数
    if page_range[0] != 1:
        page_range.insert(0, 1)# 将1插入到【0】
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 第一种方法
    blog_dates = Device.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Device.objects.filter(created_time__year=blog_date.year, 
                                        created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    devices = Device.objects.all()
    data_list = {}
    data_list_all = []
    for device in devices:
        if Data.objects.filter(device_id=device.id).exists():
            data_ob = Data.objects.filter(device_id=device.id).order_by('time').last()
            # device.data = data_ob.value
            # for data_ob in data_ob_list:
            data_list_all.append({'time': data_ob.time, 'value': data_ob.value})
            # data_list.append(data_ob.value)
            data_list[device.id] =  data_ob.value
        else:
            data_list_all.append({'time': "NULL", 'value': "NULL"})
            # data_list.append(data_ob.value)
            data_list[device.id] =  "NULL"

    context = {}
    context['blogs'] = page_of_s.object_list
    context['page_of_s'] = page_of_s
    # context['blog_types'] = BlogType.objects.all()
    # context['blog_types'] = blog_types_list
    # 直接操作数据库 真正使用前不会占用内存 而上一种方法则是在内存中进行
    context['blog_types'] = Product.objects.annotate(blog_count=Count('device')) 
    context['page_range'] = page_range
    # context['blog_dates'] = Blog.objects.dates('created_time', 'month', order = 'DESC')
    context['blog_dates'] = blog_dates_dict
    context['data_list_all'] = data_list_all
    context['data_list'] = data_list
    return context

def product_list(request):
    user_id = request.session['user_id']
    pros_all_list = Product.objects.filter(pro_user=user_id)
    count_M = Product.objects.filter(pro_user_id=user_id, protocol='MQTT').count()
    count_U = Product.objects.filter(pro_user_id=user_id, protocol='UDP').count()
    count_H = Product.objects.filter(pro_user_id=user_id, protocol='HTTP').count()
    context = get_blog_list_common_data(request, pros_all_list)
    pro_dates = Product.objects.dates('created_time', 'month', order="DESC")
    pro_dates_dict = {}
    for pro_date in pro_dates:
        pro_count = Product.objects.filter(created_time__year=pro_date.year, 
                                        created_time__month=pro_date.month).count()
        pro_dates_dict[pro_date] = pro_count
    context['count_M'] = count_M
    context['count_U'] = count_U
    context['count_H'] = count_H
    context['pro_dates'] = pro_dates_dict
    return render(request, 'dev/pro_list.html', context)

def product_internet(request, name):
    user_id = request.session['user_id']
    # print(user_id, name)
    pros_all_list = Product.objects.filter(pro_user_id=user_id, protocol=name)
    count_M = Product.objects.filter(pro_user_id=user_id, protocol='MQTT').count()
    count_U = Product.objects.filter(pro_user_id=user_id, protocol='UDP').count()
    count_H = Product.objects.filter(pro_user_id=user_id, protocol='HTTP').count()
    # count = Product.objects.filter(pro_user_id=user_id, protocol=name).count()
    context = get_blog_list_common_data(request, pros_all_list)
    context['count_M'] = count_M
    context['count_U'] = count_U
    context['count_H'] = count_H
    # context['count'] = count
    return render(request, 'dev/pro_list.html', context)
    # products = Product.objects.filter(pro_user_id=user_id, protocol=name)
    # return render(request, 'index.html', {'products': products})

def delete_product(request, id):
    Product.objects.get(id=id).delete()
    # products = Product.objects.all()
    pros_all_list = Product.objects.filter(pro_user=user_id)
    context = get_blog_list_common_data(request, pros_all_list)
    # return render(request, 'product_list.html', {'products': products})
    return render(request, 'dev/pro_list.html', context)

def delete_device(request, id):
    Device.objects.get(id=id).delete()
    devices_all_list = Device.objects.filter(product=dev_pk)
    context = get_blog_list_common_data(request, devices_all_list)
    return render(request, 'dev/device_list.html', context)

def device_list(request, dev_pk):
    devices_all_list = Device.objects.filter(product=dev_pk)
    # device_all_list = Device.objects.all()
    context = get_blog_list_common_data(request, devices_all_list)
    return render(request, 'dev/device_list.html', context)


def pros_with_date(request, year, month):
    devs_all_list = Product.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, devs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    # context['blogs'] = page_of_blogs.object_list
    return render(request, 'dev/pros_with_date.html', context)

def devs_with_date(request, year, month):
    devs_all_list = Device.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, devs_all_list)
    # pk = Device.objects.product.pk()
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    # context['pk'] = pk
    # context['blogs'] = page_of_blogs.object_list
    return render(request, 'dev/devs_with_date.html', context)

def datas_with_date(request, year, month):
    datas_all_list = Data.objects.filter(time__year=year, time__month=month)
    context = get_blog_list_common_data(request, datas_all_list)
    # pk = Device.objects.product.pk()
    context['datas_with_date'] = '%s年%s月' %(year, month)
    # context['pk'] = pk
    # context['blogs'] = page_of_blogs.object_list
    return render(request, 'dev/history.html', context)

def reg_device(request):
    if request.method == "POST":
        device_name = request.POST.get('device_name')
        product = request.POST.get('product')
        describe = request.POST.get('describe')
        authentication = request.POST.get('authentication')
        if Device.objects.filter(device_name=device_name).exists():
            context = {}
            context['flag'] = '设备名称重复'
            return render(request, 'dev/pro_form.html', context)
        else:
        # now = datetime.datetime.now()
        # print(name, product, private, number)
            # m = hashlib.md5()
            # hash_dev_id = 
            # m.update(authentication.encode(encoding="utf-8"))
            # m.update(authentication.encode(encoding="utf-8"))
            # authentication = m.hexdigest()
            Device.objects.create(device_name=device_name, pro_user = request.user, product_id=product, describe=describe, authentication=authentication)
            # 二次加密 确保唯一性
            m = hashlib.md5()
            hash_dev = Device.objects.get(device_name=device_name)
            hash_dev_id = str(hash_dev.id)
            m.update(hash_dev_id.encode(encoding="utf-8"))
            m.update(authentication.encode(encoding="utf-8"))
            authentication = m.hexdigest()
            hash_dev.authentication = authentication
            hash_dev.save()


            return redirect('product_list')
        # return render(request, 'dev/pro_form.html', context)
    else:
        products = Product.objects.all()
        context = {}
        context['products'] = products
        return render(request, 'dev/pro_form.html', context)

def history(request, dev_pk):
    datas_all_list = Data.objects.filter(device=dev_pk)
    dev_dates = Data.objects.dates('time', 'month', order="DESC")
    dev_dates_dict = {}
    for dev_date in dev_dates:
        dev_count = Data.objects.filter(time__year=dev_date.year, 
                                        time__month=dev_date.month).count()
        dev_dates_dict[dev_date] = dev_count
    # device_all_list = Device.objects.all()
    context = get_blog_list_common_data(request, datas_all_list)
    context['device_dates'] = dev_dates_dict
    return render(request, 'dev/history.html', context)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def is_online(request):
    # 获取数据
    user = request.user
    
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')
    else:
        data = {}
        data['status'] = 'SUCCESS'
        return product_list(request)





