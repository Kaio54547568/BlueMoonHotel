from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Guest, Reservation
from .forms import ReservationForm

def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'core/rooms_list.html', {'rooms': rooms})

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # tạo hoặc lấy guest theo email
            guest_email = form.cleaned_data['email']
            guest, created = Guest.objects.get_or_create(
                email=guest_email,
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'phone': form.cleaned_data.get('phone','')
                }
            )
            res = Reservation(
                guest=guest,
                room=room,
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out'],
                num_guests=form.cleaned_data['num_guests']
            )
            # tính tổng tiền đơn giản:
            nights = (res.check_out - res.check_in).days or 1
            res.total_price = nights * room.room_type.price_per_night
            res.save()
            # cập nhật trạng thái phòng
            room.status = 'reserved'
            room.save()
            return redirect('booking_success', pk=res.pk)
    else:
        form = ReservationForm()
    return render(request, 'core/book_room.html', {'room': room, 'form': form})

def booking_success(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    return render(request, 'core/booking_success.html', {'reservation': res})
