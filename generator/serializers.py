from django.db import models
from rest_framework import serializers

from .models import Group, Promo, User
from .generator import make_promo, bulk_make_promo, make_promo_json, validate_promo_params

PROMO_PARAMS_ERROR_MSG = "Параметры генератора заданы неверно, дополнительно можно указать только: {}"

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password")

    def create(self, data):
        return User.objects.create_user(username=data["username"], password=data["password"])


class GroupSerializer(serializers.ModelSerializer):
    promo = serializers.SerializerMethodField(method_name="get_promo")

    class Meta:
        fields = ("id", "group", "promo", "download")
        model = Group

    def get_promo(self, obj):
        return list(obj.promo.all().values_list("promo", flat=True))

    def get_file(self, group):
        self.update(group, {"download": make_promo_json()})
        return self


def get_group(group):
    if not isinstance(group, str) and not isinstance(group, int):
        raise serializers.ValidationError("Необходимо указать название или id группы промокодов")
    group = (Group.objects.get_or_create(group=group))[0]
    """
    if group.author != user and not group.access.filter(users=user):
        raise serializers.ValidationError("Нет прав для добавления промокодов в эту группу")"""
    return group


def create_promo(group, amount, params):
    promo_params = make_promo.__code__.co_varnames
    if not set(promo_params) >= set(params):
        raise serializers.ValidationError(PROMO_PARAMS_ERROR_MSG.format(", ".join(promo_params)))
    validate_promo_params(params)
    promo_bodies = [Promo(group=group, promo=promo) for promo in bulk_make_promo(amount, params)]
    Promo.objects.bulk_create(promo_bodies)


class PromoCheckSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field="group", read_only=True)

    class Meta:
        fields = ("group",)
        model = Promo


def validate_promo(promo):
    try:
        return Promo.objects.get(promo=promo)
    except models.ObjectDoesNotExist:
        raise serializers.ValidationError("Код не существует")
