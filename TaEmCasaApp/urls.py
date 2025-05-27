from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro_validate/', views.cadastro_validate, name='cadastro_validate'),
    path('login_validate/', views.login_validate, name='login_validate'),
    path('contato_validate/', views.contato_validate, name='contato_validate'),
    path('app/', views.app, name='app'),
    path('api/negocios/', views.negocios_json, name='negocios_json'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


