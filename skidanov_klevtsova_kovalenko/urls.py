"""skidanov_klevtsova_kovalenko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from WitcherZeroPlayerGame import views as witcher_views

urlpatterns = [
    url('ajax/get_events/', witcher_views.get_events),
    url('ajax/get_friends/', witcher_views.get_friends),
    url('ajax/generate_positive_event/', witcher_views.generate_positive_event),
    url('ajax/generate_negative_event/', witcher_views.generate_negative_event),
    url('ajax/generate_random_event/', witcher_views.generate_random_event),
    url('ajax/respawn/', witcher_views.respawn),
    url('logout/', witcher_views.logout),
    url('admin/', admin.site.urls),
    url('login/', witcher_views.login),
    url('register/', witcher_views.register),
    url('create_witcher/', witcher_views.create_witcher),
    url('home/', witcher_views.home),
    url('witcher_info/', witcher_views.witcher_info),
    url('', witcher_views.main),
]
