# api/admin.py
from django.contrib import admin
from .models import Product  # Ganti dengan model yang sesuai

admin.site.register(Product)  # Daftarkan model ke admin
