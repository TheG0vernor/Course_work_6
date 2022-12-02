from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.views import AdViewSet, CommentViewSet

router = SimpleRouter()
router.register("", AdViewSet, basename='ads')
router.register("comments", CommentViewSet, basename='comments')

urlpatterns = []

urlpatterns += router.urls
