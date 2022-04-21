from rest_framework.mixins import CreateModelMixin as Create, RetrieveModelMixin as Detail, ListModelMixin as View
from rest_framework.viewsets import GenericViewSet as Generic
from rest_framework import status
from rest_framework.response import Response

from .models import Group, User, ExtAccess
from .permissions import IsAuthorOrHasAccess, permissions
from .serializers import GroupSerializer, PromoCheckSerializer


class PromoViewSet(Generic, Create, Detail, View):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrHasAccess]

    def get_queryset(self):
        if not (user := self.request.user).is_authenticated:
            return Group.objects.none()
        has_access = ExtAccess.objects.values_list("group", flat=True).filter(users=user)
        return Group.objects.filter(author=user) | Group.objects.filter(id__in=has_access)


    def create(self, request):
        group = self.serializer_class.get_group(request.data.get("group"), user=User.objects.get(id=1))
        self.serializer_class.create(group, self.request.data.get("amount", 1), self.request.data.get("params", {}))
        serializer = self.serializer_class(group)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckView(Generic, Create):
    serializer_class = PromoCheckSerializer

    def create(self, request, *args, **kwargs):
        promo = self.serializer_class.validate(request.data.get("promo", ""))
        serializer = self.serializer_class(promo)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
