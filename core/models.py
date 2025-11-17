# backend/models.py
from django.db import models
from django.contrib.postgres.fields import CITextField

# ===== ENUM choices (map PostgreSQL ENUM sang Python choices) =====
class LoaiBienDong(models.TextChoices):
    TAM_TRU = 'tam_tru', 'Tạm trú'
    TAM_VANG = 'tam_vang', 'Tạm vắng'

class TrangThaiDotThu(models.TextChoices):
    DRAFT = 'draft', 'Nháp'
    OPEN = 'open', 'Mở'
    CLOSED = 'closed', 'Đóng'

# ===== 1) VaiTro =====
class VaiTro(models.Model):
    id_vaitro = models.IntegerField(primary_key=True)
    ten_vaitro = models.CharField(max_length=50)
    

    class Meta:
        managed = False
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
    is_deleted = models.BooleanField()

# ===== 4) NhanKhau =====
class NhanKhau(models.Model):
    id_nhankhau = models.IntegerField(primary_key=True)
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField()
    cccd = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[]  # có thể thêm RegexValidator sau nếu muốn
    )
    cccd = models.CharField(max_length=12, unique=True, null=True, blank=True)
    quan_he_chu_ho = models.CharField(max_length=50, null=True, blank=True)
    id_hokhau = models.ForeignKey(
        HoKhau, on_delete=models.RESTRICT, db_column='id_hokhau', related_name='nhan_khaus'
    )

    class Meta:
        managed = False
        db_table = 'nhankhau'
        indexes = [
            models.Index(fields=['id_hokhau'], name='idx_nhankhau_hokhau'),
        ]

    def __str__(self):
        return self.ho_ten

# ===== 5) BienDongNhanKhau =====
class BienDongNhanKhau(models.Model):
    id_biendong = models.IntegerField(primary_key=True)
    loai_biendong = models.CharField(max_length=8, choices=LoaiBienDong.choices)
    ngay_batdau = models.DateField()
    ngay_ketthuc = models.DateField(null=True, blank=True)
    ly_do = models.TextField(null=True, blank=True)
    id_nhankhau = models.ForeignKey(
        NhanKhau, on_delete=models.CASCADE, db_column='id_nhankhau', related_name='bien_dongs'
    )

# =======================
# Bảng Tài khoản
# =======================
class TaiKhoan(models.Model):
    id_taikhoan = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)  # CITEXT có thể bỏ qua
    password = models.CharField(max_length=255)
    vaitro = models.ForeignKey(VaiTro, on_delete=models.CASCADE, related_name='tai_khoan', db_column='id_vaitro')
    is_deleted = models.BooleanField()
    class Meta:
        db_table = 'taikhoan'   

# ===== 6) KhoanThu =====
class KhoanThu(models.Model):
    id_khoanthu = models.IntegerField(primary_key=True)
    ten_khoanthu = models.CharField(max_length=100)
    don_gia = models.DecimalField(max_digits=15, decimal_places=2)
    don_vi_tinh = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'khoanthu'

    def __str__(self):
        return self.ten_khoanthu

# ===== 7) DotThuPhi =====
class DotThuPhi(models.Model):
    id_dotthu = models.IntegerField(primary_key=True)
    ten_dotthu = models.CharField(max_length=100)
    ngay_batdau = models.DateField()
    ngay_ketthuc = models.DateField(null=True, blank=True)
    trang_thai = models.CharField(
        max_length=6, choices=TrangThaiDotThu.choices, default=TrangThaiDotThu.DRAFT
    )
    id_khoanthu = models.ForeignKey(
        'core.KhoanThu',             # <- dùng chuỗi
        on_delete=models.RESTRICT,
        db_column='id_khoanthu',
        related_name='dot_thus'
    )

    class Meta:
        managed = False
        db_table = 'dotthuphi'
        indexes = [
            models.Index(fields=['id_khoanthu'], name='idx_dotthu_khoanthu'),
        ]

    def __str__(self):
        return self.ten_dotthu

# ===== 8) HoaDon =====
class HoaDon(models.Model):
    id_hoadon = models.IntegerField(primary_key=True)
    tong_tien = models.DecimalField(max_digits=15, decimal_places=2)
    ngay_nop = models.DateField(null=True, blank=True)
    id_dotthu = models.ForeignKey(
        'core.DotThuPhi',            # <- dùng chuỗi
        on_delete=models.RESTRICT,
        db_column='id_dotthu',
        related_name='hoa_dons'
    )
    id_hokhau = models.ForeignKey(
        'core.HoKhau',               # <- dùng chuỗi (cho đồng bộ)
        on_delete=models.RESTRICT,
        db_column='id_hokhau',
        related_name='hoa_dons'
    )

    class Meta:
        managed = False
        db_table = 'hoadon'
        constraints = [
            models.UniqueConstraint(fields=['id_hokhau', 'id_dotthu'], name='uq_hoadon_hokhau_dotthu'),
        ]
        indexes = [
            models.Index(fields=['id_hokhau'], name='idx_hoadon_hokhau'),
            models.Index(fields=['id_dotthu'], name='idx_hoadon_dotthu'),
        ]
