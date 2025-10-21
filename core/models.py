from django.db import models

# =======================
# Bảng Hộ khẩu
# =======================
class HoKhau(models.Model):
    id_ho_khau = models.AutoField(primary_key=True)
    so_can_ho = models.CharField(max_length=50)
    dien_tich = models.DecimalField(max_digits=8, decimal_places=2)
    # id_chu_ho sẽ liên kết tới Nhân khẩu (ForeignKey tạm thời để null được)
    # ta sẽ định nghĩa sau khi có model NhanKhau

    def __str__(self):
        return f"Hộ khẩu {self.id_ho_khau} - Căn hộ {self.so_can_ho}"


# =======================
# Bảng Nhân khẩu
# =======================
class NhanKhau(models.Model):
    id_nhan_khau = models.AutoField(primary_key=True)
    id_ho_khau = models.CharField()
    # id_ho_khau = models.ForeignKey(HoKhau, on_delete=models.CASCADE, related_name='nhan_khau')
    ngay_sinh = models.DateField()
    can_cuoc_cong_dan = models.CharField(max_length=12, unique=True)
    quan_he_chu_ho = models.CharField(max_length=50)

    def __str__(self):
        return f"Nhân khẩu {self.id_nhan_khau} ({self.quan_he_chu_ho})"



# =======================
# Bảng Tài khoản
# =======================
class TaiKhoan(models.Model):
    id_tai_khoan = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    vai_tro = models.CharField(max_length=20, choices=[
        ('admin', 'Quản trị viên'),
        ('user', 'Người dùng'),
    ])

    def __str__(self):
        return f"{self.username} ({self.vai_tro})"
