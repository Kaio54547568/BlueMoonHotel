from django import forms

class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    num_guests = forms.IntegerField(min_value=1, initial=1)
