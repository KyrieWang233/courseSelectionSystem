"""test430 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from system import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^index_t/', views.index_t),
    url(r'^index_s/', views.index_s),
    url(r'^index_a/', views.index_a),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^tea1/', views.tea1),
    url(r'^tea2/', views.tea2),
    url(r'^reg_score/', views.reg),
    url(r'^stu1/', views.stu1),
    url(r'^stu2/', views.stu2),
    url(r'^stu3/', views.stu3),
    url(r'^adm1/', views.adm1),
    url(r'^adm2/', views.adm2),
]
