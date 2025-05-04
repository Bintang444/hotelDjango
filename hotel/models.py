from django.db import models

class Kamar(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)  
    deskripsi = models.TextField()
    fasilitas = models.TextField(blank=True, null=True)  
    gambar = models.ImageField(upload_to='kamar/', blank=True, null=True)

    def __str__(self):
        return self.nama

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    nama_pelanggan = models.CharField(max_length=100)
    email = models.EmailField()
    kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    total_harga = models.IntegerField()  # Field untuk total harga

    def __str__(self):
        return f"{self.nama_pelanggan} - {self.kamar.nama}"
