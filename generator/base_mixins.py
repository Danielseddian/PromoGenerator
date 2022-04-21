from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class BaseCreate(GenericViewSet, CreateModelMixin):
    pass
