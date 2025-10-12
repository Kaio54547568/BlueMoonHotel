from django.db import models
from django.utils import timezone

class RoomType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price_per_night}"

class Room(models.Model):
    STATUS = (
        ('available','Available'),
        ('occupied','Occupied'),
        ('maintenance','Maintenance'),
    )
    number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    floor = models.IntegerField(default=1)
    status = models.CharField(max_length=12, choices=STATUS, default='available')

    def __str__(self):
        return f"Room {self.number} ({self.room_type.name})"

class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Reservation(models.Model):
    STATUS = (
        ('reserved','Reserved'),
        ('checked_in','Checked-in'),
        ('checked_out','Checked-out'),
        ('cancelled','Cancelled'),
    )
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField(default=1)
    status = models.CharField(max_length=12, choices=STATUS, default='reserved')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reservation {self.id} - {self.guest} [{self.check_in} → {self.check_out}]"

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class ServiceUsage(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="services")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    qty = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
