from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accountmanage', views.accountmanage, name='accountmanage'),
    path('demomanage', views.demomanage, name='demomanage'),
    path('test/', views.test, name='test'),
    path('profile/', views.profile, name='profile'),
    
    path('hrmanage/', views.hrmanage, name='hrmanage'),
    path('hredit/', views.hredit, name='hredit'),
]
