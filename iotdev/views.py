import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse # 反向解析
# from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
# from blog.models import Blog


def home(request):
    # blog_content_type = ContentType.objects.get_for_model(Blog)
    # read_nums, dates = get_seven_days_read_data(blog_content_type)


    context = {}
    # context['dates'] = dates
    # context['read_nums'] = read_numsS
    return render(request, 'home.html', context)
