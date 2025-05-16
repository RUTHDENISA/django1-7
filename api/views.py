from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .models import Product
from .serializers import ProductSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from django_filters import rest_framework as filters

# Filter untuk Produk
class ProductFilter(filters.FilterSet):
    kode = filters.CharFilter(lookup_expr='icontains')      # filter kode mirip
    kategori = filters.CharFilter(lookup_expr='iexact')     # filter persis sama

    class Meta:
        model = Product
        fields = ['kode', 'kategori']  # field yang bisa difilter

# ViewSet untuk Produk (hanya bisa diakses jika user login dengan token)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# View untuk Registrasi (langsung kirim token)
class RegisterView(APIView):
    permission_classes = []  # supaya tidak perlu login untuk akses

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status": 201,
                "message": "Selamat anda telah terdaftar...",
                "data": {
                    "username": user.username,
                    "email": user.email,
                    "token": token.key,
                    "is_active": user.is_active,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": 400,
            "message": "Registrasi gagal",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
