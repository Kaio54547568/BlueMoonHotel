
from django.http import HttpResponse 
from calendar import day_name
from pyexpat.errors import messages
from webbrowser import get
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservationForm, KhoanThuForm
from .models import HoKhau, NhanKhau, TaiKhoan, VaiTro, KhoanThu
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse # <-- ĐÃ THÊM IMPORT NÀY
from django.contrib.auth.hashers import make_password

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def user_logout(request):
    logout(request)
#    messages.success(request, "Bạn đã đăng xuất.")
    return redirect("logintest")


@login_required(login_url="logintest")
def profile(request):
    current_user= request.user
    print(request.user.is_authenticated)
    if request.user.is_authenticated: 
        return redirect("logintest")
    return render(request, "core/profiletest.html", {
        "user": current_user
    })


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1. Kiểm tra dữ liệu
        if not username or not password1 or not password2:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Mật khẩu không khớp.")
            return redirect("register")

        if TaiKhoan.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại.")
            return redirect("register")

        # 2. Tạo tài khoản
        taikhoan = TaiKhoan.objects.create(
            username=username,
            password=make_password(password1),  # 🔐 mã hóa mật khẩu
            is_active=True,
            is_staff=False
        )

        # 3. Tự động đăng nhập sau khi đăng ký
        login(request, taikhoan)

        messages.success(request, "Đăng ký thành công!")
        return redirect("home")

    return render(request, "core/register.html")

def login_view(request):
    print("abdcsfds")
    if request.method == "POST":
        username_request = request.POST.get("username")
        password_request = request.POST.get("password")

        user = authenticate(request, username=username_request, password=password_request)
        print(username_request+'\n'+password_request)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "core/test.html", {
                "error": "Sai tên đăng nhập hoặc mật khẩu"
            })

    return render(request, "core/test.html")


# ========================================================
# 1. HÀM LOGIN & HOME (PHIÊN BẢN CHÍNH THỨC - ĐÃ FIX LỖI)
# ========================================================

# def login(request):
#     # Nếu đã có session thì vào thẳng trang chủ, không cần đăng nhập lại
#     if request.session.get('id_taikhoan'):
#         return redirect('home')

#     if request.method == 'POST':
#         # Lấy dữ liệu từ form (tên input đã khớp với file HTML mới)
#         user_nhap = None
#         if 'username_admin' in request.POST:
#             user_nhap = request.POST.get('username_admin')
#             pass_nhap = request.POST.get('password_admin')
#             vaitro_mong_muon = 1
#         elif 'username_user' in request.POST:
#             user_nhap = request.POST.get('username_user')
#             pass_nhap = request.POST.get('password_user')
#             vaitro_mong_muon = 3
        
#         if user_nhap:
#             try:
#                 tai_khoan = TaiKhoan.objects.get(username=user_nhap)
                
#                 # So sánh mật khẩu (Không mã hóa: 2005 == 2005)
#                 if pass_nhap == tai_khoan.password:
                    
#                     # Kiểm tra vai trò
#                     real_role = getattr(tai_khoan, 'id_vaitro_id', None)
#                     if real_role is None: 
#                         real_role = getattr(tai_khoan, 'vaitro_id', None)
                    
#                     if real_role == vaitro_mong_muon:
#                         # === LƯU SESSION ===
#                         request.session['id_taikhoan'] = tai_khoan.id_taikhoan
#                         # Các dòng này đảm bảo Session được lưu chặt chẽ
#                         request.session.modified = True 
#                         request.session.save()
                        
#                         # === CHUYỂN HƯỚNG VỀ TRANG CHỦ ===
#                         if real_role == 3:
#                             return redirect('accountant_home')
#                         else:
#                             return redirect('home')
#                     else:
#                         messages.error(request, "Bạn đang đăng nhập sai vai trò!")
#                 else:
#                     messages.error(request, "Mật khẩu không đúng!")

#             except TaiKhoan.DoesNotExist:
#                 messages.error(request, "Tên đăng nhập không tồn tại!")
        
#     return render(request, 'core/login.html')

def home(request):
    # # Kiểm tra bảo mật: Chưa đăng nhập thì đuổi về Login
    # id_tk = request.session.get('id_taikhoan')
    # if not id_tk:
    #     return redirect('login')
        
    # Đã đăng nhập -> Hiển thị trang chủ
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/home.html', {'home': HoKhaus})

def accountant_home(request):
    # Kiểm tra bảo mật
    id_tk = request.session.get('id_taikhoan')
    if not id_tk:
         return redirect('login')
         
    return render(request, 'core/Accountant.html')

# ========================================================
# 2. CÁC HÀM CHỨC NĂNG KHÁC (GIỮ NGUYÊN)
# ========================================================

def test(request):
    ds_ho_khau = HoKhau.objects.all()
    return render(request, 'core/test.html', {'ho_khau_list': ds_ho_khau})

def edit_nhan_khau(request, id_nhankhau):
    nk = get_object_or_404(NhanKhau, id_nhankhau=id_nhankhau)
    if request.method == "POST":
        nk.ho_ten = request.POST.get('ho_ten')
        nk.ngay_sinh = request.POST.get('ngay_sinh') or None
        nk.cccd = request.POST.get('cccd') or None
        nk.quan_he_chu_ho = request.POST.get('quan_he_chu_ho') or None
        ho_khau_id = request.POST.get('ho_khau_id')

        if ho_khau_id:
            nk.id_hokhau_id = ho_khau_id

        nk.save()
        return redirect('nhan_khau_profile', id_nhankhau=nk.id_nhankhau)

    return render(request, 'core/demomanage_edit.html', {'nhan_khau': nk})

def nhan_khau_profile(request, id_nhankhau):
    nhan_khau = get_object_or_404(NhanKhau, id_nhankhau=id_nhankhau)
    return render(request, 'core/nhan_khau_profile.html', {'nhan_khau': nhan_khau})

def nhan_khau_delete(request, id_nhankhau):
    exists = NhanKhau.objects.filter(id_nhankhau=id_nhankhau).exists()
    if(exists):
        nhan_khau = get_object_or_404(NhanKhau, id_nhankhau=id_nhankhau)
        nhan_khau.is_deleted=True
    return render(request, 'core/demomanage_delete.html')

def add_demo(request):
    if request.method == "POST":
        ho_ten = request.POST.get('ho_ten')
        ngay_sinh = request.POST.get('ngay_sinh')
        cccd = request.POST.get('cccd')
        quan_he_chu_ho = request.POST.get('quan_he_chu_ho')
        ho_khau_id = request.POST.get('ho_khau_id')

        try:
            hokhau = HoKhau.objects.get(id_hokhau=ho_khau_id)
            NhanKhau.objects.create(
                ho_ten=ho_ten,
                ngay_sinh=ngay_sinh or None,
                cccd=cccd or None,
                quan_he_chu_ho=quan_he_chu_ho or None,
                ho_khau=hokhau
            )
        except HoKhau.DoesNotExist:
            pass 

        return redirect('demomanage/adddemo')   

    return render(request, 'core/demomanage_add.html')
# def login(request):
#     # Xử lý khi người dùng NHẤN NÚT (gửi form)
#     if request.method == 'POST':
        
#         # Xác định xem form Admin hay User được gửi
#         if 'username_admin' in request.POST:
#             user_nhap = request.POST.get('username_admin')
#             pass_nhap = request.POST.get('password_admin')
#             # Đảm bảo tên vai trò này KHỚP CHÍNH XÁC với CSDL của bạn
#             vaitro_mong_muon = 1 # (1 = admin)
        
#         elif 'username_user' in request.POST:
#             user_nhap = request.POST.get('username_user')
#             pass_nhap = request.POST.get('password_user')
#             # Đảm bảo tên vai trò này KHỚP CHÍNH XÁC với CSDL của bạn
#             vaitro_mong_muon = 3 # (3 = kế toán, hoặc vai trò người dùng)
        
#         else:
#             user_nhap = None

#         if user_nhap:
#             try:
#                 # Bước 2: Tìm tài khoản trong CSDL
#                 tai_khoan = TaiKhoan.objects.get(username=user_nhap) 
                
#                 # Bước 3: Kiểm tra mật khẩu
#                 if pass_nhap == tai_khoan.password:
                    
#                     # === SỬA LẠI DÒNG NÀY ===
#                     # Bước 4: Kiểm tra vai trò (So sánh SỐ với SỐ)
#                     if tai_khoan.vaitro_id == vaitro_mong_muon:
#                     # === KẾT THÚC SỬA ===
                        
#                         # BƯỚC 5: ĐĂNG NHẬP
#                         # Dùng hàm 'auth_login' chúng ta đã import
#                         request.session['id_taikhoan'] = tai_khoan.id_taikhoan
                        
#                         # Dựa theo thông tin trước đó, 1=Admin, 3=Kế toán
                        
#                         if vaitro_mong_muon == 3: # NẾU LÀ KẾ TOÁN
#                             return redirect('accountant_home') # <-- Đi đến trang Kế toán
#                         else: # NẾU LÀ ADMIN HOẶC VAI TRÒ KHÁC
#                             return redirect('home') # <-- Đi đến trang chủ chung
#                     else:
#                         # Vai trò sai
#                         messages.error(request, "Bạn đang đăng nhập ở form không đúng vai trò!")
#                 else:
#                     # Mật khẩu sai
#                     messages.error(request, "Mật khẩu không đúng!")

#             except TaiKhoan.DoesNotExist:
#                 # Không tìm thấy username
#                 messages.error(request, "Tên đăng nhập không tồn tại!")
        
#         # Nếu có bất kỳ lỗi nào, render lại trang login
#         # (Template sẽ tự động hiển thị các 'messages' lỗi)
#         return render(request, 'core/login.html')

#     else:
#         # Xử lý khi người dùng MỞ TRANG (yêu cầu GET)
#         # Chỉ cần hiển thị trang login
#         return render(request, 'core/login.html')

def demomanage(request):
    nhan_khau_list = NhanKhau.objects.all()
    query = request.GET.get('search_id', 'demomanage')
    if query:
        try:
            for a in nhan_khau_list:
                if(a.id_nhankhau==int(query)):
                    nhan_khau_list= [a]
        except ValueError:
            nhan_khau_list = NhanKhau.objects.all()

    context = {
        'nhan_khau_list': nhan_khau_list,
        'query': query,
    }
    return render(request, 'core/demomanage.html', context)
def demomanage_delete(request, id_hokhau):
    exists = HoKhau.objects.filter(id_hokhau=id_hokhau).exists()
    if(exists):
        hr = get_object_or_404(HoKhau, id_hokhau=id_hokhau)
        hr.is_deleted=True
    return render(request, 'core/hrmanage_delete.html')

def accountmanage(request):
    tai_khoan_list = TaiKhoan.objects.all()
    query = request.GET.get('search_id', 'hrmanage')
    if query:
        try:
            for a in tai_khoan_list:
                if(a.id_taikhoan==int(query)):
                    tai_khoan_list= [a]
        except ValueError:
            tai_khoan_list= TaiKhoan.objects.all()
    
    context = {
        'tai_khoan_list': tai_khoan_list,
        'query': query,
    }

    return render(request, 'core/accountmanage.html', context)

def accountmanage_delete(request, id_taikhoan):
    exists = TaiKhoan.objects.filter(id_taikhoan=id_taikhoan).exists()
    if(exists):
        account = get_object_or_404(TaiKhoan, id_taikhoan=id_taikhoan)
        account.is_deleted=True
    return render(request, 'core/accountmanage_delete.html')

def accountmanage_addaccount(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password_raw = request.POST.get('password') 
        vaitro_id = request.POST.get('vaitro_id')

        try:
            vaitro = VaiTro.objects.get(id_vaitro=vaitro_id)
            TaiKhoan.objects.create(
                username=username,
                password=password_raw,
                vaitro=vaitro
            )
            messages.success(request, f"Tài khoản '{username}' đã được thêm thành công!")
        except VaiTro.DoesNotExist:
            messages.error(request, "ID vai trò không tồn tại!")

        return redirect('/accountmanage/addaccount')

    return render(request, 'core/accountmanage_addaccount.html')

def view_taikhoan(request, id_taikhoan):

    user = authenticate(request, username="admin", password="2005")
    login(request, user)
    
    taikhoan = get_object_or_404(TaiKhoan, id_taikhoan=id_taikhoan)
    return render(request, 'core/accountmanage_view.html', {'taikhoan': taikhoan})

def edit_taikhoan(request, id_taikhoan):
    taikhoan = get_object_or_404(TaiKhoan, id_taikhoan=id_taikhoan)

    if request.method == "POST":
        username = request.POST.get('username')
        password_raw = request.POST.get('password')
        vaitro_id = request.POST.get('vaitro_id')

        taikhoan.username = username
        if password_raw.strip():
            taikhoan.password = password_raw

        try:
            vaitro = VaiTro.objects.get(id_vaitro=vaitro_id)
            taikhoan.vaitro = vaitro
        except VaiTro.DoesNotExist:
            messages.error(request, "ID vai trò không tồn tại.")
            return redirect('edit_taikhoan', id_taikhoan=id_taikhoan)

        taikhoan.save()
        messages.success(request, f"Đã cập nhật thông tin cho tài khoản {username}.")
        return redirect('edit_taikhoan', id_taikhoan=id_taikhoan)

    return render(request, 'core/accountmanage_change.html', {'taikhoan': taikhoan})

def hredit(request):
    nhan_khau_list = HoKhau.objects.all()
    return render(request, 'core/hredit.html', {'nhan_khau_list': nhan_khau_list})

def hrmanage(request):
    ds_ho_khau = HoKhau.objects.all()
    query = request.GET.get('search_id', 'hrmanage')
    if query:
        try:
            for a in ds_ho_khau:
                if(a.id_hokhau==int(query)):
                    ds_ho_khau= [a]
        except ValueError:
            ds_ho_khau = HoKhau.objects.all()
    
    context = {
        'ho_khau_list': ds_ho_khau,
        'query': query,
    }

    return render(request, 'core/hrmanage.html', context)

def hrmanage_delete(request, id_hokhau):
    exists = HoKhau.objects.filter(id_hokhau=id_hokhau).exists()
    if(exists):
        hr = get_object_or_404(HoKhau, id_hokhau=id_hokhau)
        hr.is_deleted=True
    return render(request, 'core/hrmanage_delete.html')

def add_hokhau(request):
    if request.method == "POST":
        so_can_ho = request.POST.get('so_can_ho')
        dien_tich = request.POST.get('dien_tich')

        if so_can_ho:
            try:
                dien_tich_value = float(dien_tich) if dien_tich else None
                HoKhau.objects.create(so_can_ho=so_can_ho, dien_tich=dien_tich_value)
                messages.success(request, f"Hộ khẩu căn {so_can_ho} đã được thêm thành công!")
            except ValueError:
                messages.error(request, "Giá trị diện tích không hợp lệ!")
        else:
            messages.error(request, "Vui lòng nhập số căn hộ!")

        return redirect('add_hokhau')

    return render(request, 'core/add_hokhau.html')

def hokhau_detail(request, id_hokhau):
    hokhau = get_object_or_404(HoKhau, id_hokhau=id_hokhau)
    thanh_vien = NhanKhau.objects.filter(ho_khau=hokhau)

    return render(request, 'core/hokhau_detail.html', {
        'hokhau': hokhau,
        'thanh_vien': thanh_vien
    })


def edit_hokhau(request, id_hokhau):
    hokhau = get_object_or_404(HoKhau, id_hokhau=id_hokhau)

    if request.method == "POST":
        so_can_ho = request.POST.get("so_can_ho")
        dien_tich = request.POST.get("dien_tich")

        if not so_can_ho:
            messages.error(request, "Số căn hộ không được để trống!")
        else:
            try:
                hokhau.so_can_ho = so_can_ho
                hokhau.dien_tich = float(dien_tich) if dien_tich else None
                hokhau.save()
                messages.success(request, "Cập nhật thông tin hộ khẩu thành công!")
                return redirect('hokhau_detail', id_hokhau=id_hokhau)
            except ValueError:
                messages.error(request, "Diện tích phải là số hợp lệ!")

    return render(request, 'core/hokhau_edit.html', {'hokhau': hokhau})

def HoKhaus_list(request):
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/HoKhaus_list.html', {'HoKhaus': HoKhaus})

def profile(request):
    profile = NhanKhau.objects.all()
    return render(request, 'core/profile.html', {'profile': profile})


def fee_collection_period(request):
    return render(request, 'core/FeeCollectionPeriod.html')
def statistics_view(request):
    return render(request, 'core/Statistics.html')
def fee_management(request):
    khoan_thu_list = KhoanThu.objects.all()
    total_count = khoan_thu_list.count()
    form = KhoanThuForm()
    context = {
        'khoan_thu_list': khoan_thu_list, 
        'total_count': total_count,      
        'form': form, 
    }
    return render(request, 'core/FeeManagement.html', context)

def view_khoanthu_detail_modal(request, pk):
    khoan_thu = get_object_or_404(KhoanThu, id_khoanthu=pk) 
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pass 
    return render(request, 'core/ViewFeeDetailModal.html', {'khoan_thu': khoan_thu})

def add_khoanthu(request):
    if request.method == 'POST':
        form = KhoanThuForm(request.POST)
        if form.is_valid():
            khoan_thu = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
                messages.success(request, "Khoản thu mới đã được tạo thành công!")
                return HttpResponse(status=200)
            else:
                return redirect('fee_management')
        else:
            context = {'form': form}
            return render(request, 'core/AddFeeModal.html', context) 
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = KhoanThuForm()
        context = {'form': form}
        return render(request, 'core/AddFeeModal.html', context)
    else:
        form = KhoanThuForm()
        context = {'form': form, 'page_title': "TẠO KHOẢN THU MỚI"}
        return render(request, 'core/AddFee.html', context)

def edit_khoanthu(request, pk):
    khoan_thu = get_object_or_404(KhoanThu, id_khoanthu=pk) 

    if request.method == 'POST':
        form = KhoanThuForm(request.POST, instance=khoan_thu)
        
        if form.is_valid():
            form.save() 
            messages.success(request, f"Khoản thu '{khoan_thu.ten_khoanthu}' đã được cập nhật thành công!")
            return HttpResponse(status=200) 
        else:
            context = {'form': form, 'khoan_thu': khoan_thu}
            return render(request, 'core/EditFeeModal.html', context)
            
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = KhoanThuForm(instance=khoan_thu)
        context = {'form': form, 'khoan_thu': khoan_thu}
        return render(request, 'core/EditFeeModal.html', context) 
    else:
        form = KhoanThuForm(instance=khoan_thu)
        context = {
            'form': form, 
            'khoan_thu': khoan_thu,
            'page_title': f"CHỈNH SỬA KHOẢN THU - {khoan_thu.ten_khoanthu}",
        }
        return render(request, 'core/EditFee.html', context)