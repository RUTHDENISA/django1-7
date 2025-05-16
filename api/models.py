# api/models.py
from django.db import models

class Product(models.Model):
    kode = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=100)
    kategori = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    status_menu = models.BooleanField(default=True)  # bisa juga pakai CharField

    def __str__(self):
        return self.nama