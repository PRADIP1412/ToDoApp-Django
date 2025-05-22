"""
URL configuration for ToDoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('task_list/', views.task_list, name="task_list"),
    path('create_task/', views.create_task, name="create_task"),
    path('update/<int:task_id>/', views.update_task_view, name='update_task'), # New
    path('complete/<int:task_id>/', views.complete_task_view, name='complete_task'), # Updated for POST
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'), # Updated for POST
]