from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.views import AdViewSet, CommentViewSet, ads_user

router = SimpleRouter()
router.register("", AdViewSet, basename='ads')
router.register("comments", CommentViewSet, basename='comments')

urlpatterns = [
    path("me/", ads_user, name='ads_user')
]

urlpatterns += router.urls
