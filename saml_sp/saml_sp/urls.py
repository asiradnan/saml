from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saml2/', include('djangosaml2.urls')),
    path('', views.home, name='home'),
    path('protected/', views.protected, name='protected'),
    path('api/user-profile/', views.user_profile_api, name='user_profile_api'),
    path('logout/', views.simple_logout, name='simple_logout'),
    path('health/', views.health_check, name='health_check'),
]
