from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/<int:kamar_id>/', views.booking, name='booking'),
    path('kamar/<int:kamar_id>/', views.detail_kamar, name='detail_kamar'),
    path('lihat_pesanan/', views.lihat_pesanan, name='lihat_pesanan'),
    path('update_booking/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('pesanan/konfirmasi/<int:booking_id>/', views.konfirmasi_pesanan, name='konfirmasi_pesanan'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('invoice/<int:booking_id>/', views.cetak_invoice, name='invoice'),
    ]
