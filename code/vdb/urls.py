"""capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.vdbIndex, name='vdbIndex'),
    url(r'^/createTable', views.createTable, name='createTable'),
    url(r'^/updateTable', views.updateTable, name='updateTable'),
    url(r'^/deleteTable', views.deleteTable, name='deleteTable'),
    url(r'^/viewTable', views.viewTable, name='viewTable'),
    url(r'^/renameTable', views.renameTable, name='renameTable'),
    url(r'^/renameColumn', views.renameColumn, name='renameColumn'),
    url(r'^/insertColumn', views.insertColumn, name='insertColumn'),
    url(r'^/deleteColumn', views.deleteColumn, name='deleteColumn'),
    #url(r'^/insertRecordIntoColumn', views.insertRecordIntoColumn, name='insertRecordIntoColumn')
]
