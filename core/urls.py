from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accountmanage', views.accountmanage, name='accountmanage'),
    path('accountmanage/addaccount', views.accountmanage_addaccount, name='accountmanage_addaccount'),
    path('accountmanage/change/<int:id_taikhoan>/', views.edit_taikhoan, name='edit_taikhoan'),
    path('accountmanage/view/<int:id_taikhoan>/', views.view_taikhoan, name='view_taikhoan'),  # 👈 thêm dòng này


    path('demomanage', views.demomanage, name='demomanage'),
    path('demomanage/adddemo', views.add_demo, name='demomanage/adddemo'),
    path('nhan-khau/<int:id_nhankhau>/', views.nhan_khau_profile, name='nhan_khau_profile'),
    path('nhan-khau/delete/<int:id_nhankhau>/', views.nhan_khau_delete, name='nhan_khau_delete'),
    path('nhan-khau/<int:id_nhankhau>/edit/', views.edit_nhan_khau, name='edit_nhan_khau'),  

    path('test/', views.test, name='test'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),

    path('hrmanage/', views.hrmanage, name='hrmanage'),
    path('ho-khau/them/', views.add_hokhau, name='add_hokhau'),

    path('hredit/', views.hredit, name='hredit'),
]
