from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accountmanage', views.accountmanage, name='accountmanage'),
    path('accountmanage/addaccount', views.accountmanage_addaccount, name='accountmanage_addaccount'),
    # alias:
    path('accountmanage/addaccount/', views.accountmanage_addaccount, name='addaccount'),
    path('accountmanage/change/<int:id_taikhoan>/', views.edit_taikhoan, name='edit_taikhoan'),
    path('accountmanage/view/<int:id_taikhoan>/', views.view_taikhoan, name='view_taikhoan'),  
    path('accountmanage/delete/<int:id_taikhoan>/', views.accountmanage_delete, name='accountmanage_delete'),  


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
    path('hokhau_detail/<int:id_hokhau>/', views.hokhau_detail, name='hokhau_detail'),
    path('ho-khau/<int:id_hokhau>/edit/', views.edit_hokhau, name='hokhau_edit'),
    path('ho-khau/<int:id_hokhau>/delete/', views.hrmanage_delete, name='hrmanage_delete'),


    path('hredit/', views.hredit, name='hredit'),



    #============Kế toán URLs===================
    path('accountant-home/', views.accountant_home, name='accountant_home'),  # Accountant main page

    path('fee-management/', views.fee_management, name='fee_management'),  # Trang quản lý khoản thu
    path('fee-management/add/', views.add_khoanthu, name='add_khoanthu'),
    path('fee-management/detail/<int:pk>/modal/', views.view_khoanthu_detail_modal, name='view_khoanthu_detail_modal'), 
    path('fee-management/edit/<int:pk>/', views.edit_khoanthu, name='edit_khoanthu'),

    path('fee-collection-period/', views.fee_collection_period, name='fee_collection_period'),  # Trang quản lý đợt thu phí
    path('statistics-view/', views.statistics_view, name='statistics_view'),  # Trang thống kê
    
]
