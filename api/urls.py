from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RegisterView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('api-token-auth/', obtain_auth_token),  # untuk login jika diperlukan
]
