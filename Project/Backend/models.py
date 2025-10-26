from django.db import models

# =================================================================
# BẢNG 1: VaiTro
# Chức năng: Lưu trữ các vai trò (quyền hạn) trong hệ thống.
# =================================================================
class VaiTro(models.Model):
    ten_vaitro = models.CharField(max_length=50, null=False, blank=False, verbose_name="Tên vai trò")

    def __str__(self):
        # Hiển thị tên vai trò trên trang Admin
        return self.ten_vaitro

    class Meta:
        verbose_name = "Vai trò"
        verbose_name_plural = "1. Các vai trò"

# =================================================================
# BẢNG 2: TaiKhoan
# Chức năng: Lưu trữ thông tin tài khoản để đăng nhập.
# =================================================================
class TaiKhoan(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="Tên đăng nhập")
    password = models.CharField(max_length=255, null=False, blank=False, verbose_name="Mật khẩu")
    
    # Quan hệ Nhiều-1: Một VaiTro có nhiều TaiKhoan
    vaiTro = models.ForeignKey(VaiTro, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vai trò")

    def __str__(self):
        return self.username

    def is_ke_toan(self):
        """Kiểm tra tài khoản này có phải là Kế toán không."""
        return self.vaiTro and self.vaiTro.ten_vaitro.lower() == 'kế toán'

    def is_to_truong(self):
        """Kiểm tra tài khoản này có phải là Tổ trưởng không."""
        return self.vaiTro and 'tổ trưởng' in self.vaiTro.ten_vaitro.lower()

    class Meta:
        verbose_name = "Tài khoản"
        verbose_name_plural = "2. Các tài khoản"

# =================================================================
# BẢNG 3: HoKhau
# Chức năng: Quản lý thông tin của từng hộ gia đình.
# =================================================================
class HoKhau(models.Model):
    so_can_ho = models.CharField(max_length=20, unique=True, null=False, blank=False, verbose_name="Số căn hộ")
    dien_tich = models.FloatField(null=True, blank=True, verbose_name="Diện tích (m2)")

    def __str__(self):
        return self.so_can_ho

    def get_thanh_vien_list(self):
        """Lấy danh sách tất cả nhân khẩu (QuerySet) thuộc hộ này."""
        return self.nhankhau_set.all()

    def get_chu_ho(self):
        """Tìm và trả về đối tượng NhanKhau là 'Chủ hộ' của hộ này."""
        try:
            return self.nhankhau_set.get(quan_he_chu_ho__iexact='Chủ hộ')
        except NhanKhau.DoesNotExist:
            return None

    def get_so_luong_thanh_vien(self):
        """Đếm tổng số nhân khẩu đang ở trong hộ này."""
        return self.nhankhau_set.count()

    class Meta:
        verbose_name = "Hộ khẩu"
        verbose_name_plural = "3. Quản lý Hộ khẩu"

# =================================================================
# BẢNG 4: NhanKhau
# Chức năng: Lưu thông tin chi tiết của từng cư dân (nhân khẩu).
# =================================================================
class NhanKhau(models.Model):
    ho_ten = models.CharField(max_length=100, null=False, blank=False, verbose_name="Họ và tên")
    ngay_sinh = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    CanCuocCongDan = models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name="Số CCCD")
    quan_he_chu_ho = models.CharField(max_length=50, null=True, blank=True, verbose_name="Quan hệ với chủ hộ")
    
    # Quan hệ Nhiều-1: Một HoKhau có nhiều NhanKhau
    # on_delete=models.CASCADE: Nếu xóa HoKhau, tất cả NhanKhau liên quan sẽ bị xóa theo.
    hoKhau = models.ForeignKey(HoKhau, on_delete=models.CASCADE, verbose_name="Thuộc hộ khẩu")

    def __str__(self):
        return self.ho_ten

    class Meta:
        verbose_name = "Nhân khẩu"
        verbose_name_plural = "4. Quản lý Nhân khẩu"

# =================================================================
# BẢNG 5: BienDongNhanKhau
# Chức năng: Ghi nhận lịch sử tạm trú, tạm vắng của cư dân.
# =================================================================
class BienDongNhanKhau(models.Model):
    # Cung cấp các lựa chọn cố định cho trường 'loai_biendong'
    LOAI_BIEN_DONG_CHOICES = [
        ('Tạm trú', 'Tạm trú'),
        ('Tạm vắng', 'Tạm vắng'),
    ]
    
    loai_biendong = models.CharField(max_length=20, choices=LOAI_BIEN_DONG_CHOICES, verbose_name="Loại biến động")
    ngay_batdau = models.DateField(null=False, verbose_name="Ngày bắt đầu")
    ngay_ketthuc = models.DateField(null=True, blank=True, verbose_name="Ngày kết thúc")
    ly_do = models.TextField(null=True, blank=True, verbose_name="Lý do")
    
    # Quan hệ Nhiều-1: Một NhanKhau có thể có nhiều BienDongNhanKhau
    nhanKhau = models.ForeignKey(NhanKhau, on_delete=models.CASCADE, verbose_name="Nhân khẩu")

    def __str__(self):
        return f"{self.loai_biendong} - {self.nhanKhau.ho_ten}"

    class Meta:
        verbose_name = "Biến động nhân khẩu"
        verbose_name_plural = "5. Quản lý Biến động"

# =================================================================
# BẢNG 6: KhoanThu (Bảng "Một")
# Chức năng: Định nghĩa các loại phí dịch vụ (ví dụ: Phí quản lý).
# =================================================================
class KhoanThu(models.Model):
    # Cung cấp các lựa chọn cố định cho trường 'don_vi_tinh'
    DON_VI_TINH_CHOICES = [
        ('m2', 'Theo mét vuông (m2)'),
        ('hộ', 'Theo hộ gia đình'),
        ('người', 'Theo số nhân khẩu'),
    ]

    ten_khoanthu = models.CharField(max_length=100, null=False, verbose_name="Tên khoản thu")
    don_gia = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Đơn giá (VND)")
    don_vi_tinh = models.CharField(max_length=20, choices=DON_VI_TINH_CHOICES, null=False, verbose_name="Đơn vị tính")

    def __str__(self):
        return f"{self.ten_khoanthu} ({self.don_gia} VND / {self.don_vi_tinh})"
        
    class Meta:
        verbose_name = "Khoản thu"
        verbose_name_plural = "6. Quản lý Khoản thu"

# =================================================================
# BẢNG 7: DotThuPhi (Bảng "Nhiều")
# Chức năng: Quản lý các đợt thu phí được tạo ra theo kỳ.
# =================================================================
class DotThuPhi(models.Model):
    TRANG_THAI_CHOICES = [
        ('Đang diễn ra', 'Đang diễn ra'),
        ('Đã kết thúc', 'Đã kết thúc'),
        ('Chưa bắt đầu', 'Chưa bắt đầu'),
    ]

    ten_dotthu = models.CharField(max_length=100, null=False, verbose_name="Tên đợt thu")
    ngay_batdau = models.DateField(null=False, verbose_name="Ngày bắt đầu")
    ngay_ketthuc = models.DateField(null=True, blank=True, verbose_name="Ngày kết thúc")
    trang_thai = models.CharField(max_length=50, choices=TRANG_THAI_CHOICES, default='Chưa bắt đầu', verbose_name="Trạng thái")
    
    # Quan hệ Một-Nhiều: Một KhoanThu có nhiều DotThuPhi
    # on_delete=models.CASCADE: Nếu xóa KhoanThu, các ĐợtThu liên quan cũng bị xóa.
    khoanThu = models.ForeignKey(
        KhoanThu, 
        on_delete=models.CASCADE, 
        verbose_name="Thuộc khoản thu"
    )

    def __str__(self):
        return f"{self.ten_dotthu} ({self.khoanThu.ten_khoanthu})"
        
    def tinh_tong_da_thu(self):
        """Thống kê tổng số tiền ĐÃ NỘP trong đợt thu này."""
        tong = self.hoadon_set.filter(trang_thai='Đã nộp').aggregate(models.Sum('tong_tien'))['tong_tien__sum']
        return tong or 0

    def tinh_tong_cong_no(self):
        """Thống kê tổng số tiền CÒN NỢ trong đợt thu này."""
        tong = self.hoadon_set.filter(trang_thai='Chưa nộp').aggregate(models.Sum('tong_tien'))['tong_tien__sum']
        return tong or 0
        
    def get_so_ho_da_nop(self):
        """Đếm số lượng hóa đơn đã được thanh toán trong đợt này."""
        return self.hoadon_set.filter(trang_thai='Đã nộp').count()

    class Meta:
        verbose_name = "Đợt thu phí"
        verbose_name_plural = "7. Quản lý Đợt thu phí"

# =================================================================
# BẢNG 8: HoaDon
# Chức năng: Ghi nhận việc thanh toán của một hộ cho một đợt thu.
# =================================================================
class HoaDon(models.Model):
    TRANG_THAI_HOA_DON_CHOICES = [
        ('Đã nộp', 'Đã nộp'),
        ('Chưa nộp', 'Chưa nộp'),
    ]
    
    tong_tien = models.DecimalField(max_digits=15, decimal_places=2, null=False, verbose_name="Tổng tiền (VND)")
    ngay_nop = models.DateField(null=True, blank=True, verbose_name="Ngày nộp")
    trang_thai = models.CharField(max_length=50, choices=TRANG_THAI_HOA_DON_CHOICES, default='Chưa nộp', verbose_name="Trạng thái")
    
    # Quan hệ Nhiều-1: Một HoKhau có nhiều HoaDon
    # on_delete=models.SET_NULL: Nếu xóa HoKhau, hóa đơn vẫn giữ lại nhưng không liên kết nữa.
    hoKhau = models.ForeignKey(HoKhau, on_delete=models.SET_NULL, null=True, verbose_name="Hộ khẩu")
    
    # Quan hệ Nhiều-1: Một DotThuPhi có nhiều HoaDon
    dotThuPhi = models.ForeignKey(DotThuPhi, on_delete=models.CASCADE, verbose_name="Thuộc đợt thu")

    def __str__(self):
        return f"Hóa đơn {self.hoKhau.so_can_ho} - {self.dotThuPhi.ten_dotthu}"

    class Meta:
        verbose_name = "Hóa đơn"
        verbose_name_plural = "8. Quản lý Hóa đơn"