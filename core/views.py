from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservationForm
from .models import HoKhau, NhanKhau, TaiKhoan


def test(request):
    ds_ho_khau = HoKhau.objects.all()  # Lấy toàn bộ dữ liệu tro bảng HoKhau
    ds_ho_khau =[
        {"id_ho_khau": 1, "so_can_ho": "A101", "dien_tich": 85.5},
        {"id_ho_khau": 2, "so_can_ho": "A102", "dien_tich": 90.0},
        {"id_ho_khau": 3, "so_can_ho": "B203", "dien_tich": 78.2},
    ]

    return render(request, 'core/test.html', {'ho_khau_list': ds_ho_khau})

def demomanage(request):
    nhan_khau_list = NhanKhau.objects.all()
    nhan_khau_list = [
        NhanKhau(1, 1, "1990-05-10", "012345678901", "Chủ hộ"),
        NhanKhau(2, 1, "1995-07-21", "012345678902", "Vợ"),
        NhanKhau(3, 1, "2010-11-03", "012345678903", "Con"),
        NhanKhau(4, 1, "1988-01-15", "012345678904", "Anh trai"),
        NhanKhau(5, 1, "1992-09-29", "012345678905", "Em gái"),
        NhanKhau(6, 1, "1975-12-11", "012345678906", "Bố"),
        NhanKhau(7, 1, "1978-06-05", "012345678907", "Mẹ"),
        NhanKhau(8, 1, "2000-02-22", "012345678908", "Con trai"),
        NhanKhau(9, 1, "2002-03-14", "012345678909", "Con gái"),
        NhanKhau(10,1,  "1983-08-19", "012345678910", "Cô"),
    ]

    query = request.GET.get('search_id', 'demomanage')
    if query:
        try:
            print(query)
            # lọc theo ID nhân khẩu nếu người dùng nhập
            for a in nhan_khau_list:
                if(a.id_nhan_khau==int(query)):
                    nhan_khau_list= [a]
                    print(a.id_nhan_khau)
                print(a.id_nhan_khau)
        except ValueError:
          nhan_khau_list = [
            NhanKhau(1, 1, "1990-05-10", "012345678901", "Chủ hộ"),
            NhanKhau(2, 1, "1995-07-21", "012345678902", "Vợ"),
            NhanKhau(3, 1, "2010-11-03", "012345678903", "Con"),
            NhanKhau(4, 1, "1988-01-15", "012345678904", "Anh trai"),
            NhanKhau(5, 1, "1992-09-29", "012345678905", "Em gái"),
            NhanKhau(6, 1, "1975-12-11", "012345678906", "Bố"),
            NhanKhau(7, 1, "1978-06-05", "012345678907", "Mẹ"),
            NhanKhau(8, 1, "2000-02-22", "012345678908", "Con trai"),
            NhanKhau(9, 1, "2002-03-14", "012345678909", "Con gái"),
            NhanKhau(10,1,  "1983-08-19", "012345678910", "Cô"),
        ]    
        # nhan_khau_list = NhanKhau.objects.all()  # nếu không nhập, hiển thị tất cả

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
    tai_khoan_list = [
        TaiKhoan(1, "admin", "123456", "admin"),
        TaiKhoan(2, "chuho1", "abc123", "user"),
        TaiKhoan(3, "user01", "pass01", "user"),
        TaiKhoan(4, "user02", "pass02", "user"),
        TaiKhoan(5, "user03", "pass03", "user"),
        TaiKhoan(6, "user04", "pass04", "user"),
        TaiKhoan(7, "user05", "pass05", "user"),
        TaiKhoan(8, "user06", "pass06", "user"),
        TaiKhoan(9, "user07", "pass07", "user"),
        TaiKhoan(10, "user08", "pass08", "user"),
    ]
    return render(request, 'core/accountmanage.html', {'tai_khoan_list': tai_khoan_list })
def hredit(request):
    nhan_khau_list = HoKhau.objects.all()
    nhan_khau_list = [
        NhanKhau(1, 1, "1990-05-10", "012345678901", "Chủ hộ"),
        NhanKhau(2, 1, "1995-07-21", "012345678902", "Vợ"),
        NhanKhau(3, 1, "2010-11-03", "012345678903", "Con"),
        NhanKhau(4, 1, "1988-01-15", "012345678904", "Anh trai"),
        NhanKhau(5, 1, "1992-09-29", "012345678905", "Em gái"),
        NhanKhau(6, 1, "1975-12-11", "012345678906", "Bố"),
        NhanKhau(7, 1, "1978-06-05", "012345678907", "Mẹ"),
        NhanKhau(8, 1, "2000-02-22", "012345678908", "Con trai"),
        NhanKhau(9, 1, "2002-03-14", "012345678909", "Con gái"),
        NhanKhau(10,1,  "1983-08-19", "012345678910", "Cô"),
    ]
    return render(request, 'core/hredit.html', {'nhan_khau_list': nhan_khau_list})
def hrmanage(request):
    ds_ho_khau = HoKhau.objects.all()  # Lấy toàn bộ dữ liệu tro bảng HoKhau
    ds_ho_khau = [       
        {"id_ho_khau": 1, "so_can_ho": "A101", "dien_tich": 85.5},
        {"id_ho_khau": 2, "so_can_ho": "A102", "dien_tich": 90.0},
        {"id_ho_khau": 3, "so_can_ho": "B203", "dien_tich": 78.2},
        {"id_ho_khau": 4, "so_can_ho": "A101", "dien_tich": 85.5},
        {"id_ho_khau": 5, "so_can_ho": "A102", "dien_tich": 90.0},
        {"id_ho_khau": 6, "so_can_ho": "B203", "dien_tich": 78.2},
    ]
    return render(request, 'core/hrmanage.html', {'ho_khau_list': ds_ho_khau})
def HoKhaus_list(request):
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/HoKhaus_list.html', {'HoKhaus': HoKhaus})
def home(request):
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/home.html', {'home': home})
def profile(request):
    HoKhaus = HoKhau.objects.all()
    return render(request, 'core/profile.html', {'profile': profile})
