# api/serializers.py
from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'kode', 'nama', 'kategori', 'harga', 'status_menu']
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password tidak cocok")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username sudah dipakai")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

