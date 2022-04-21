import json
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response

from .base_mixins import BaseCreate
from .models import Group, User, ExtAccess
from .permissions import IsAuthorOrHasAccess, permissions
from .serializers import GroupSerializer, PromoCheckSerializer, UserSerializer, get_group, create_promo, validate_promo


class CreateUserView(BaseCreate):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class PromoViewSet(BaseCreate, RetrieveModelMixin, ListModelMixin):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrHasAccess]

    def get_queryset(self):
        if not (user := self.request.user).is_authenticated:
            return Group.objects.none()
        has_access = ExtAccess.objects.values_list("group", flat=True).filter(users=user)
        return user.promo_group.all() | Group.objects.filter(id__in=has_access)

    def create(self, request):
        group = get_group((req_get := request.data.get)("group"), user=User.objects.get(id=1))
        create_promo(group, req_get("amount", 1), req_get("params", {}))
        self.serializer_class(group).get_file(group)
        headers = self.get_success_headers((serializer := self.serializer_class(group)).data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckView(BaseCreate):
    serializer_class = PromoCheckSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        promo = validate_promo(request.data.get("promo", ""))
        headers = self.get_success_headers((serializer := self.serializer_class(promo)).data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
