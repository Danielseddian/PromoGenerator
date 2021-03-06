import json
import secrets
import string
import os
from rest_framework import serializers

from PromoGenerator.settings import MEDIA_ROOT
from .models import Promo, Group

PROMO_SHORT_MSG = "Длинна промокода без учёта префикса должна быть не меньше 5 знаков, заданная длинна - {}"
PROMO_LONG_MSG = "Длинна промокода с учётом префикса не может быть больше 120 знаков, заданная длинна - {}"


def validate_promo_params(length=20, prefix="", symbols=string.ascii_letters + string.digits + "!#$%&-_", exclude=""):
    if not (
        isinstance(length, int) and isinstance(prefix, str) and isinstance(symbols, str) and isinstance(exclude, str)
    ):
        raise serializers.ValidationError("Параметры указаны неверно")
    if length > 120:
        raise serializers.ValidationError(PROMO_LONG_MSG.format(length))
    length -= len(prefix)
    if length < 5:
        raise serializers.ValidationError(PROMO_SHORT_MSG.format(length))


def make_promo(length=20, prefix="", symbols=string.ascii_letters + string.digits + "!#$%&-_", exclude=""):
    length -= len(prefix)
    symbols = symbols.translate({ord(excluding): None for excluding in exclude})
    return prefix + "".join(secrets.choice(symbols) for _ in range(length))


def bulk_make_promo(amount=1, params={}, promos=None):
    if not promos:
        promos = Promo.objects.all().values_list("promo", flat=True)
    new_promos = []
    while amount:
        promo = make_promo(**params)
        if promo not in promos and promo not in new_promos:
            new_promos.append(promo)
            amount -= 1
    return new_promos


def make_promo_json():
    groups = Group.objects.all()
    data = {group.group: list(group.promo.values_list("promo", flat=True)) for group in groups}
    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)
    file_name = "promo.json"
    with open(MEDIA_ROOT + "\\" + file_name, 'w', encoding='utf-8') as file:
        file.write(
            json.dumps(data, ensure_ascii=False))
    return file_name
