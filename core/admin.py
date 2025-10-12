from django.contrib import admin
from .models import RoomType, Room, Guest, Reservation, Service, ServiceUsage

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number','room_type','floor','status')
    list_filter = ('status','room_type')

admin.site.register(RoomType)
admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Service)
admin.site.register(ServiceUsage)
