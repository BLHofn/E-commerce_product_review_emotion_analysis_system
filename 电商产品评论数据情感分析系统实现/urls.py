"""电商产品评论数据情感分析系统实现 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path(r'',views.index),
    path('admin/', admin.site.urls),
    path('login/', views.login,name='login'),
    path('index/', views.index,name='index'),
    path('grjs/',views.grjs,name='grjs'),
    path('lyb/',views.lyb,name='lyb'),
    path('sl/',views.sl,name='sl'),
    path('xx/',views.xx,name='xx'),
    path('mp3/',views.mp3,name='mp3'),
    path('bsxx/',views.bsxx,name='bsxx'),
]
