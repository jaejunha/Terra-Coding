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
	url(r'^$', views.printDir, name='printDir'),
    url(r'^/printDir', views.printDir, name='sourceView'),
    url(r'^/printProblem', views.printProblem, name='printProblem'),
    url(r'^/solveProblem', views.solveProblem, name='solveProblem'),
    url(r'^/solveEdit', views.solveEdit, name='solveEdit'),
    url(r'^/sourceView', views.sourceView, name='sourceView'),
    url(r'^/sourceEdit', views.sourceEdit, name='sourceEdit'),
    url(r'^/sourceDel', views.sourceDel, name='sourceDel'),
    url(r'^/renameFile', views.renameFile, name='renameFile'),
    url(r'^/createNewFile', views.createNewFile, name='createNewFile'),
    url(r'^/compile_res', views.compiler_connector, name='compile_res')
]
