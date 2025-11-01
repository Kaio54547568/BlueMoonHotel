from django.db import models

class VaiTro(models.Model):
    id_vaitro = models.AutoField(primary_key=True)
    ten_vaitro = models.CharField(max_length=50)
    class Meta:
        db_table = 'vaitro'   
    def __str__(self):
        return self.ten_vaitro
# =======================
# Bảng Hộ khẩu
# =======================
class HoKhau(models.Model):
    id_hokhau = models.AutoField(primary_key=True)
    so_can_ho = models.CharField(max_length=20)
    dien_tich = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'hokhau'   
    def __str__(self):
        return f"Hộ khẩu {self.id_hokhau} - Căn {self.so_can_ho}"
# =======================
# Bảng Nhân khẩu
# =======================
class NhanKhau(models.Model):
    id_nhankhau = models.AutoField(primary_key=True)
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField(null=True, blank=True)
    cccd = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[]  # có thể thêm RegexValidator sau nếu muốn
    )
    quan_he_chu_ho = models.CharField(max_length=50, null=True, blank=True)
    ho_khau = models.ForeignKey(
        'HoKhau',
        on_delete=models.CASCADE,
        db_column='id_hokhau'  # 👉 trỏ tới đúng tên cột trong PostgreSQL
    )
    class Meta:
        db_table = 'nhankhau'   

    def __str__(self):
        return f"{self.ho_ten} (ID: {self.id_nhankhau})"

# =======================
# Bảng Tài khoản
# =======================
class TaiKhoan(models.Model):
    id_taikhoan = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)  # CITEXT có thể bỏ qua
    password = models.CharField(max_length=255)
    vaitro = models.ForeignKey(VaiTro, on_delete=models.CASCADE, related_name='tai_khoan', db_column='id_vaitro')
    class Meta:
        db_table = 'taikhoan'   
    def __str__(self):
        return self.username
    
#KẾ TOÁN

# =======================
# Bảng Khoản thu
# =======================
class KhoanThu(models.Model):
    id_khoanthu = models.AutoField(
        primary_key=True,
        verbose_name="Mã Khoản Thu",
    )
    ten_khoanthu = models.CharField(
        max_length=300,
        verbose_name="Tên Khoản Thu",
        blank=False, #Không được để trống
    )
    
    don_gia = models.DecimalField(
        max_digits=30,
        decimal_places=0, #Không có chữ số thập phân
        blank=False, #Không được để trống
        verbose_name="Đơn Giá (VND)"
    )
    UNIT_CHOICES = [
        ('per_person', 'Mỗi người'),
        ('per_apartment', 'Mỗi căn hộ'),
        ('per_month', 'Hàng tháng'),
        ('per_year', 'Hàng năm'),
        ('per_quarter', 'Hàng quý'),
        ('fixed', 'Cố định'),
    ]
    don_vi_tinh = models.CharField(
        max_length=50, 
        choices=UNIT_CHOICES, 
        default='fixed',
        blank=False, #Không được để trống
        verbose_name="Đơn Vị Tính/Kỳ Hạn"
    )

    class Meta:
        verbose_name = "Khoản Thu"
        verbose_name_plural = "Khoản Thu"
        ordering = ['ten_khoanthu']
        db_table = 'khoanthu'

    def __str__(self):
        return self.ten_khoanthu
    