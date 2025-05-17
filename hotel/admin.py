from django.contrib import admin
from django.contrib import messages
from .models import Kamar, Booking

@admin.register(Kamar)
class KamarAdmin(admin.ModelAdmin):
    list_display = ('nama', 'harga')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'nama_pelanggan', 'email', 'alamat', 'kamar', 'check_in', 'check_out', 'total_harga', 'metode_pembayaran', 'bukti_pembayaran')
    list_display = ('nama_pelanggan', 'kamar', 'status', 'check_in', 'check_out', 'metode_pembayaran', 'bukti_pembayaran')
    list_filter = ('status', 'metode_pembayaran')
    search_fields = ('nama_pelanggan', 'email', 'kamar__nama', 'status')  # search bar nama, email, kamar, status

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