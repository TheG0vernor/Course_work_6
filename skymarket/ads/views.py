from rest_framework import pagination, viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad, Comment
from ads.serializers import CommentSerializer, AdSerializer, AdDetailSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    pagination_class = AdPagination
    queryset = Ad.objects.all()
    permission_classes([IsAuthenticated])

    serializer_classes = {
        'retrieve': AdDetailSerializer
    }
    default_serializer = AdSerializer
    default_permission = [AllowAny()]
    # permissions = {
    #     ...
    # }

    # def get(self, request, *args, **kwargs):
    #     self.queryset = self.queryset.order_by('-created_at')  # если не будет работать вернуться и подключить внешние таблицы. перед этим подключить super().

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    # def get_permissions(self):
    #     return self.permissions.get(self.action, self.default_permission)

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author=request.user)
        return super().list(self, request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
