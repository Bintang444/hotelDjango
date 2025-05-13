from django.shortcuts import render, get_object_or_404, redirect
from .models import Kamar, Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def konfirmasi_pesanan(request, booking_id):
    if not request.user.is_staff:  # Pastikan hanya admin yang bisa mengonfirmasi
        return redirect('hotel:home')  # Arahkan ke halaman utama jika bukan admin

    pesanan = get_object_or_404(Booking, id=booking_id)
    pesanan.status = 'Confirmed'
    pesanan.save()
    return redirect('hotel:lihat_pesanan')  # Arahkan kembali ke halaman daftar pesanan setelah mengonfirmasi

@login_required
def lihat_pesanan(request):
    if request.user.is_staff:
        # Admin bisa lihat semua pesanan
        bookings = Booking.objects.all()
    else:
        # User biasa hanya lihat pesanannya sendiri
        bookings = Booking.objects.filter(user=request.user)

    for booking in bookings:
        durasi = (booking.check_out - booking.check_in).days
        booking.total_harga = booking.kamar.harga * durasi

    return render(request, 'lihat_pesanan.html', {'bookings': bookings})

@login_required
def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status != 'Pending':
        return redirect('hotel:lihat_pesanan')

    if request.method == 'POST':
        kamar_id = request.POST['kamar']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        try:
            kamar_baru = Kamar.objects.get(id=kamar_id)
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')

            if check_out_date <= check_in_date:
                messages.error(request, "Tanggal check-out harus lebih besar dari check-in.")
                return redirect('hotel:update_booking', booking_id=booking.id)

            durasi = (check_out_date - check_in_date).days
            total_harga = kamar_baru.harga * durasi

            # Update semua field
            booking.kamar = kamar_baru
            booking.check_in = check_in_date
            booking.check_out = check_out_date
            booking.total_harga = total_harga
            booking.save()

            messages.success(request, "Booking berhasil diupdate.")
            return redirect('hotel:lihat_pesanan')

        except Exception as e:
            messages.error(request, f"Gagal update booking: {str(e)}")

    kamars = Kamar.objects.all()
    return render(request, 'update_booking.html', {'booking': booking, 'kamars': kamars})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status == 'Pending':
        booking.status = 'Cancelled'
        booking.save()

    return redirect('hotel:lihat_pesanan')  # balik ke halaman pesanan


def homepage(request):
    # Ambil semua data kamar
    kamars = Kamar.objects.all()
    return render(request, 'homepage.html', {'kamars': kamars})

def detail_kamar(request, kamar_id):
    kamar = get_object_or_404(Kamar, id=kamar_id)
    return render(request, 'detail_kamar.html', {'kamar': kamar})

@login_required
def booking(request, kamar_id):
    kamar = get_object_or_404(Kamar, id=kamar_id)
    if request.method == 'POST':
        nama_pelanggan = request.POST['nama_pelanggan']
        email = request.POST['email']  # <- bagian ini bisa diganti
        alamat = request.POST['alamat']  # Ambil alamat dari form

        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        
        # Convert string tanggal ke objek datetime
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        
        # Hitung durasi menginap
        duration = (check_out_date - check_in_date).days
        
        # Hitung total harga (harga per malam * durasi)
        total_harga = kamar.harga * duration
        
        # Buat booking baru
        Booking.objects.create(
            user=request.user,  # Ambil user yang sedang login
            nama_pelanggan=nama_pelanggan,
            email=email,
            alamat=alamat,
            kamar=kamar,
            check_in=check_in_date,
            check_out=check_out_date,
            status='Pending',
            total_harga=total_harga  # Masukkan total harga ke dalam booking
        )
        
        return redirect('hotel:homepage')

    return render(request, 'booking.html', {'kamar': kamar})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']  # Ambil nama depan
        last_name = request.POST['last_name']  # Ambil nama belakang

        if password != password2:
            messages.error(request, 'Password tidak cocok!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah dipakai!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,  # Set nama depan
                last_name=last_name,    # Set nama belakang
            )
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('hotel:login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('hotel:homepage')
        else:
            messages.error(request, 'Username atau Password salah!')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('hotel:homepage')


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa # type: ignore

def cetak_invoice(request, booking_id):
    from hotel.models import Booking  # atau sesuaikan
    booking = Booking.objects.get(id=booking_id)
    template = get_template('invoice_template.html')
    html = template.render({'booking': booking})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{booking_id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Gagal buat PDF')
    return response