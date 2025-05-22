from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cadastro_validate/', views.cadastro_validate, name='cadastro_validate'),
    path('login_validate/', views.login_validate, name='login_validate'),
    path('contato_validate/', views.contato_validate, name='contato_validate'),
    path('app/', views.app, name='app'),
    path('api/negocios/', views.negocios_json, name='negocios_json'),
]
