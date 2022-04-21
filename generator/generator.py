import secrets
import string

from .models import Promo


def make_promo(prefix="", length=20, excludes="", symbols=string.printable[:-6]):
    length -= len(prefix)
    symbols = symbols.translate({ord(exclude): None for exclude in excludes})
    return prefix + ''.join(secrets.choice(symbols) for _ in range(length))


def bulk_make_promo(amount, params):
    promos = Promo.objects.all().values_list("promo")
    new_promos = []
    while amount:
        promo = make_promo(**params)
        if promo not in promos and promo not in new_promos:
            new_promos.append(promo)
            amount -= 1
    return new_promos
