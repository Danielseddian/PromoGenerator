from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers

from generator.models import Group, Promo
from generator.generator import validate_promo_params, bulk_make_promo, make_promo_json

SYMBOLS_HELP_TEXT = "Символы, из которых будет формироваться промокод, по умолчанию все буквы и цыфры + «!#$%&-_»"
EXCLUDE_HELP_TEXT = "Исключения, которые будут исключены из формирования промокода, подходит для символов по умолчанию"


class Command(BaseCommand):
    help = "Генератор промокодов"

    def add_arguments(self, parser):
        parser.add_argument("amount", type=int, help="Количество промокодов.")
        parser.add_argument("group", type=str, help="Группа, для которой будут созданы промокоды")

        parser.add_argument("-l", "--length", type=int, help="Длинна промокода, по умолчанию - 20")
        parser.add_argument("-p", "--prefix", type=str, help="Префикс, если требуется")
        parser.add_argument("-s", "--symbols", type=str, help=SYMBOLS_HELP_TEXT)
        parser.add_argument("-e", "--exclude", type=str, help=EXCLUDE_HELP_TEXT)

    def handle(self, *args, **kwargs):
        if length := kwargs["length"]:
            kwargs["length"] = int(length)

        amount = int(kwargs["amount"])
        group = kwargs["group"]
        params = {key: value for key in ("length", "prefix", "symbols", "exclude") if (value := kwargs.get(key))}
        try:
            validate_promo_params(**params)
        except serializers.ValidationError as exc:
            self.stdout.write(self.style.ERROR(exc.detail))
            return

        group = Group.objects.get_or_create(group=group)[0]
        promo_bodies = [Promo(group=group, promo=promo) for promo in bulk_make_promo(amount, params)]
        promos = Promo.objects.bulk_create(promo_bodies)
        make_promo_json()
        self.stdout.write(
            self.style.SUCCESS(f"Новые промокоды для группы {group}:\n" + "\n".join((promo.promo for promo in promos)))
        )
