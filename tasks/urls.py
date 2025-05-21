from django.urls import path
from .views import home, singup, singout, singin, tasks_completed, tasks_pending, create_task, task_update, task_complete, task_delete

urlpatterns = [
    path('', home, name = 'home'),
    path('singup/', singup, name = 'register'),
    path('singout/', singout, name = 'logout'),
    path('singin/', singin, name = 'login'),
    path('tasks_completed/', tasks_completed, name = 'tasks_completed'),
    path('tasks_pending/', tasks_pending, name = 'tasks_pending'),
    path('tasks/<int:task_id>/', task_update, name = 'task_update'),
    path('tasks/<int:task_id>/complete/', task_complete, name = 'task_complete'),
    path('tasks/<int:task_id>/delete/', task_delete, name = 'task_delete'),
    path('tasks/create/', create_task, name = 'create_task'),
]