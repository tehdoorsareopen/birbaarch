from django.urls import path

from .views import index

app_name = 'taskmanager'

urlpatterns = [
    path('index/', index)
]
