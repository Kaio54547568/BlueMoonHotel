import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlueMoonHotel.settings')
django.setup()

from myapp.models import KhoanThu

# ví dụ lấy dữ liệu
print(list(KhoanThu.objects.values()))
