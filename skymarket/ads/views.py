from rest_framework import pagination, viewsets
from rest_framework.decorators import permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad, Comment
from ads.permissions import AdPermission
from ads.serializers import CommentSerializer, AdSerializer, AdDetailSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    pagination_class = AdPagination
    queryset = Ad.objects.all()

    serializer_classes = {
        'retrieve': AdDetailSerializer
    }
    default_serializer = AdSerializer
    default_permission = [AllowAny()]

    permissions = {
        'create': [IsAuthenticated(), AdPermission()],
        'update': [IsAuthenticated(), AdPermission()],
        'partial_update': [IsAuthenticated(), AdPermission()],
        'destroy': [IsAuthenticated(), AdPermission()]  # IsAdminUser() - встроенная permission администратор ли user. допускается использовать | в качестве или.
    }

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.select_related('author').order_by('-created_at')

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    # другой способ:
    # def get_serializer_class(self):
    #     if self.action in ['retrieve']:
    #         return AdDetailSerializer
    #     else:
    #         return AdSerializer

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        self.queryset = Ad.objects.filter(author=request.user)
        return super().list(self, request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    default_permission = [AllowAny()]

    permissions = {
        'create': [IsAuthenticated(), AdPermission()],
        'update': [IsAuthenticated(), AdPermission()],
        'partial_update': [IsAuthenticated(), AdPermission()],
        'destroy': [IsAuthenticated(), AdPermission()]
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_queryset(self):
        ad_id = self.kwargs.get('ad_pk')  # идёт связка с полем ad из Comment, которое также указано в lookup
        return self.queryset.filter(ad_id=ad_id)

    def perform_create(self, serializer):  # написание коммента
        ad_id = self.kwargs.get('ad_pk')
        ad_instance = get_object_or_404(queryset=Ad, pk=ad_id)
        user_id = self.request.user
        serializer.save(author=user_id, ad=ad_instance)
