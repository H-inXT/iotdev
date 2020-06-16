from emq.client import client_main
from emq.server import server_main
from django.http import HttpResponse
from time import sleep


def start_server(request):
    server_main()
    return HttpResponse('启动服务成功')


def stop_server(request):
    server_stop()
    return HttpResponse('关闭服务成功')


def start_client(request, dev_id, key):
    count = 5
    while count:
        client_main(dev_id, key)
        sleep(10)
        count -= 1
    return HttpResponse('发送数据结束')

