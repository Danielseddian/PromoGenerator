from django.db import models
from rest_framework import serializers

from .models import Group, Promo, User
from .generator import make_promo, bulk_make_promo, make_promo_txt

PROMO_PARAMS_ERROR_MSG = "Параметры генератора заданы неверно, дополнительно можно указать только: {}"
PROMO_LEN_ERROR_MSG = "Для надёжности длинна промокода без учёта префикса должна быть не меньше 5, заданная длинна - {}"


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
        self.update(group, {"download": make_promo_txt(self.data)})
        return self


def get_group(group, user):
    if not isinstance(group, str) and not isinstance(group, int):
        raise serializers.ValidationError("Необходимо указать название или id группы промокодов")
    group = (Group.objects.filter(group=group) or [Group.objects.create(group=group, author=user)])[0]
    if group.author != user and not group.access.filter(users=user):
        raise serializers.ValidationError("Нет прав для добавления промокодов в эту группу")
    return group


def create_promo(group, amount, params):
    promo_params = make_promo.__code__.co_varnames
    if not set(promo_params) >= set(params):
        raise serializers.ValidationError(PROMO_PARAMS_ERROR_MSG.format(", ".join(promo_params)))
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