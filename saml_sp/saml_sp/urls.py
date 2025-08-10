from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saml2/', include('djangosaml2.urls')),
    path('', views.home, name='home'),
    path('protected/', views.protected, name='protected'),
]
