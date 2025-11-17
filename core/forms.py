from django import forms

from .models import KhoanThu


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    num_guests = forms.IntegerField(min_value=1, initial=1)

class KhoanThuForm(forms.ModelForm):
    class Meta:
        model = KhoanThu
        fields = ['ten_khoanthu', 'don_gia', 'don_vi_tinh'] 
        widgets = {
            'ten_khoanthu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên khoản thu'}),
            'don_gia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập đơn giá (VND)'}),
            'don_vi_tinh': forms.Select(attrs={'class': 'form-control'}),
        }