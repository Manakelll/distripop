"""
URL configuration for Atrium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name ="index"),
    path('distribution/', views.distribution, name="distribution"),
    path('recherche/', views.recherche, name="recherche_distribution"),
    path('modifier_distribution/', views.modifier_distribution, name='modifier_distribution'),
    path('creation/', views.creer_beneficiaire, name="creation"),
    path('crediter/', views.crediter, name="crediter"),
    path('parametre/', views.parametre, name="parametre"),
    path('creer_distribution/', views.creer_distribution, name="creer_distribution"),
    path('verification_validite/', views.verification_validite, name="verification_validite"),
    path('del_aide/', views.del_aide, name="del_aide"),
    path('del_baide/', views.del_baide, name="del_baide"),
    path('recherche_parametre/', views.recherche_parametre, name="recherche_parametre"),
    path('modifier_beneficiaire/', views.modifier_beneficiaire, name='modifier_beneficiaire'),
    path('maj_beneficiaire/', views.maj_beneficiaire, name='maj_beneficiaire'),
    path('cree_beneficiaire/', views.cree_beneficiaire, name="cree_beneficiaire"),
    path('attribuer_aide/', views.attributer_aide, name="attribuer_aide"),
    path('creer_aide/', views.creer_aide, name='creer_aide'),
    path('modifier_aide/', views.modifier_aide, name="modifier_aide"),
    path('get_radio_choices/', views.get_radio_choices, name='get_radio_choices'),
]
