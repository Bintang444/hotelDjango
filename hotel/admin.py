from django.contrib import admin
from django.contrib import messages
from .models import Kamar, Booking

@admin.register(Kamar)
class KamarAdmin(admin.ModelAdmin):
    list_display = ('nama', 'harga')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('nama_pelanggan', 'kamar', 'status', 'check_in', 'check_out')
    search_fields = ('nama_pelanggan', 'email', 'kamar__nama', 'status')  # search bar by nama, email, kamar, status

    def save_model(self, request, obj, form, change):
        if change:
            original = Booking.objects.get(pk=obj.pk)
            if original.status == 'Cancelled' and obj.status != 'Cancelled':
                self.message_user(
                    request,
                    "❌ Pesanan yang sudah dibatalkan tidak bisa diubah statusnya.",
                    level=messages.ERROR
                )
                return
        super().save_model(request, obj, form, change)

