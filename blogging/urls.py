from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowViewSet
from .views_auth import RegisterView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"follow", FollowViewSet, basename="follow")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
]
