from django.contrib import admin

from booking.models import Room, BookingUser


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number_or_title', 'cost', 'population')


class BookingUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date_start', 'date_end')


admin.site.register(Room, RoomAdmin)
admin.site.register(BookingUser, BookingUserAdmin)
