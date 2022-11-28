from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import pagination, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad, Comment
from ads.serializers import CommentSerializer, AdSerializer, AdDetailSerializer
from skymarket.settings import PAGE_SIZE
from users.models import User


# class AdPagination(pagination.PageNumberPagination):
#     pass


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_classes = {
        'retrieve': AdDetailSerializer
    }
    default_serializer = AdSerializer
    # default_permission = [AllowAny()]
    # permissions = {
    #     ...
    # }

    # def get(self, request, *args, **kwargs):
    #     self.queryset = self.queryset.order_by('-created_at')  # если не будет работать вернуться и подключить внешние таблицы. перед этим подключить super().

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    # def get_permissions(self):
    #     return self.permissions.get(self.action, self.default_permission)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def ads_user(request):
    user_qs = User.objects.annotate(ads=Count('ad'))
    paginator = Paginator(object_list=user_qs, per_page=PAGE_SIZE)
    page_number = request.GET.page('page', 1)
    page_object = paginator.get_page(page_number)

    ads = [{
        "id": i.id,
        "name": i.first_name,
        "ads": i.ads,
    } for i in page_object]

    response = {"count": paginator.count,
                "results": ads,
                }
    return JsonResponse(data=response, json_dumps_params={'ensure_ascii': False})

