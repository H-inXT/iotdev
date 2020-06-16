from django.urls import path
from emq import views

urlpatterns = [
    path('startServer', views.start_server, name='startServer'),
    path('startClient/<int:dev_id>/<str:key>',views.start_client, name='startClient'),
    path('stopServer',views.stop_server, name='stopServer'),
]
