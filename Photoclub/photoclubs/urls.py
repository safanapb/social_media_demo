"""Photoclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AdminUserViewSet, TagViewSet, PostCreationViewSet, PostListViewSet, UserLikeViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'user-creation', UserViewSet, basename='user-creation')
router.register(r'admin-creation', AdminUserViewSet, basename='admin-creation')
router.register(r'tag', TagViewSet, basename="tag")
router.register(r'post-creation', PostCreationViewSet, basename='post-creation')
router.register(r'post-listing', PostListViewSet, basename='post-listing')
router.register(r'post-like', UserLikeViewSet, basename='post-like')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
