from django.urls import path

from .views import (
    create_task, complete_task, reassign_tasks,
    view_task, user_tasks, index
)

app_name = 'taskmanager'

urlpatterns = [
    path('index/', index, name='index'),
    path('my-tasks/', user_tasks, name='my_tasks'),
    path('create/', create_task, name='create_task'),
    path('reassign/', reassign_tasks, name='reassign_tasks'),
    path('view/<int:task_id>', view_task, name='view_task'),
    path('complete/<int:task_id>', complete_task, name='complete_task'),
    # path('auth/login/', login, name='login'),
]
