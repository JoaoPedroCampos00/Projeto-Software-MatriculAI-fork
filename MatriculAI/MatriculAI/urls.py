"""
URL configuration for MatriculAI project.

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

from django.contrib import admin
from django.urls import path
from MatriculAI import views
from django.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name="home"),
    path('duvidas/', views.paginaDuvidas, name="paginaDuvidas"),
    path('cadastro/', views.paginaCadastro, name="paginaCadastro"),
    path('matricula/', views.matricula, name="matricula"),
    #path('MatriculAI/', include('MatriculAI.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='MatriculAI/login.html'), name='login'),
    path('accounts/signup/', views.paginaCadastro, name='criar_conta'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.paginaLogin, name='paginaLogin'),
    path('matricula/addTurma', views.addTurma),
    path('matricula/testarPossibilidades', views.testarPossibilidades),
    path('matricula/ant', views.proxTabela),
]
