from pyexpat.errors import messages
from webbrowser import get
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservationForm
from .models import HoKhau, NhanKhau, TaiKhoan, VaiTro
from django.contrib import messages


def test(request):
    ds_ho_khau = HoKhau.objects.all()  # Lấy toàn bộ dữ liệu tro bảng HoKhau

    return render(request, 'core/test.html', {'ho_khau_list': ds_ho_khau})
def edit_nhan_khau(request, id_nhankhau):
    nhan_khau = get_object_or_404(NhanKhau, id_nhankhau=id_nhankhau)

    if request.method == "POST":
        nhan_khau.ho_ten = request.POST.get('ho_ten')
        nhan_khau.ngay_sinh = request.POST.get('ngay_sinh') or None
        nhan_khau.cccd = request.POST.get('cccd') or None
        nhan_khau.quan_he_chu_ho = request.POST.get('quan_he_chu_ho') or None
        ho_khau_id = request.POST.get('ho_khau_id')

        if ho_khau_id:
            try:
                nhan_khau.ho_khau = HoKhau.objects.get(id_hokhau=ho_khau_id)
            except HoKhau.DoesNotExist:
                pass

        nhan_khau.save()
        return redirect('nhan_khau_profile', id_nhankhau=nhan_khau.id_nhankhau)

    return render(request, 'core/edit_nhan_khau.html', {'nhan_khau': nhan_khau})

def nhan_khau_profile(request, id_nhankhau):
    nhan_khau = get_object_or_404(NhanKhau, id_nhankhau=id_nhankhau)
    return render(request, 'core/nhan_khau_profile.html', {'nhan_khau': nhan_khau})

def nhan_khau_delete(request, id_nhankhau):
    exists = NhanKhau.objects.filter(id_nhankhau=id_nhankhau).exists()
    if(exists):
        nhan_khau = get_object_or_404(NhanKhau, id_nhankhau=id_nhankhau)
        nhan_khau.delete()
    return render(request, 'core/nhan_khau_delete.html')

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
            pass  # có thể hiển thị thông báo lỗi sau

        return redirect('demomanage/adddemo')  # reload lại form trống    

    return render(request, 'core/add_demo.html')
def login(request):

    ds_ho_khau = HoKhau.objects.all()  # Lấy toàn bộ dữ liệu tro bảng HoKhau
    return render(request, 'core/login.html', {'ho_khau_list': ds_ho_khau})

def demomanage(request):
    nhan_khau_list = NhanKhau.objects.all()
    for nhan_khau in nhan_khau_list:
        print(nhan_khau.id_nhankhau)
    # nhan_khau_list = [
    #             NhanKhau(1, "nguyen van a", "1990-05-10", "012345678901", "Chủ hộ", 1),
    #             NhanKhau(2, "nguyen van a", "1995-07-21", "012345678902", "Vợ", 1),
    #             NhanKhau(3, "nguyen van a", "2010-11-03", "012345678903", "Con", 1),
    #             NhanKhau(4, "nguyen van a", "1988-01-15", "012345678904", "Anh trai", 1),
    #             NhanKhau(5, "nguyen van a", "1992-09-29", "012345678905", "Em gái", 1),
    #             NhanKhau(6, "nguyen van a", "1975-12-11", "012345678906", "Bố", 1),
    #             NhanKhau(7, "nguyen van a", "1978-06-05", "012345678907", "Mẹ", 1),
    #             NhanKhau(8, "nguyen van a", "2000-02-22", "012345678908", "Con trai", 1),
    #             NhanKhau(9, "nguyen van a", "2002-03-14", "012345678909", "Con gái", 1),
    #             NhanKhau(10,"nguyen van a",  "1983-08-19", "012345678910", "Cô", 1),
    #         ]
    query = request.GET.get('search_id', 'demomanage')
    if query:
        try:
            print(query)
            # lọc theo ID nhân khẩu nếu người dùng nhập
            for a in nhan_khau_list:
                if(a.id_nhankhau==int(query)):
                    nhan_khau_list= [a]
                    print(a.id_nhankhau)
                print(a.id_nhankhau)
        except ValueError:
            nhan_khau_list = NhanKhau.objects.all()  # nếu không nhập, hiển thị tất cả

    context = {
        'nhan_khau_list': nhan_khau_list,
        'query': query,
    }
    # for a in nhan_khau_list: 
    #     print(a.id_ho_khau)
    return render(request, 'core/demomanage.html', context)
def accountmanage(request):
    # Dữ liệu mẫu cho Tài khoản
    tai_khoan_list = TaiKhoan.objects.all()
    return render(request, 'core/accountmanage.html', {'tai_khoan_list': tai_khoan_list })
def accountmanage_addaccount(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        vaitro_id = request.POST.get('vaitro_id')

        try:
            vaitro = VaiTro.objects.get(id_vaitro=vaitro_id)
            TaiKhoan.objects.create(
                username=username,
                password=password,
                vaitro=vaitro
            )
            messages.success(request, f"Tài khoản '{username}' đã được thêm thành công!")
        except VaiTro.DoesNotExist:
            messages.error(request, "ID vai trò không tồn tại!")

        return redirect('/accountmanage/addaccount')

    return render(request, 'core/accountmanage_addaccount.html')

def view_taikhoan(request, id_taikhoan):
    taikhoan = get_object_or_404(TaiKhoan, id_taikhoan=id_taikhoan)
    return render(request, 'core/accountmanage_view.html', {'taikhoan': taikhoan})
def edit_taikhoan(request, id_taikhoan):
    taikhoan = get_object_or_404(TaiKhoan, id_taikhoan=id_taikhoan)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        vaitro_id = request.POST.get('vaitro_id')

        taikhoan.username = username
        if password.strip():  # chỉ cập nhật nếu có nhập mật khẩu mới
            taikhoan.password = password

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
    ds_ho_khau = HoKhau.objects.all()  # Lấy toàn bộ dữ liệu tro bảng HoKhau
    return render(request, 'core/hrmanage.html', {'ho_khau_list': ds_ho_khau})
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

def HoKhaus_list(request):
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/HoKhaus_list.html', {'HoKhaus': HoKhaus})
def home(request):
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/home.html', {'home': home})
def profile(request):
    profile = NhanKhau.objects.all()
    return render(request, 'core/profile.html', {'profile': profile})
