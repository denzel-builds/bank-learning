from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', lambda request: redirect('task-list')),

    path('tasks/', views.task_list, name='task-list'),
    path('tasks/create/', views.task_create, name='task-create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task-update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task-delete'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),

    path('api/tasks/', views.api_task_list, name='api-task-list'),
    path('api/tasks/create/', views.api_create_task, name='api-task-create'),
    path('api/tasks/<int:pk>/update/', views.api_update_task, name='api-task-update'),
    path('api/tasks/<int:pk>/delete/', views.api_delete_task, name='api-task-delete'),
    

    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', lambda request: redirect('task-list')),
    
]