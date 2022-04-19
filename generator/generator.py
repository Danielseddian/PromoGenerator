import secrets
import string


def make_secret(prefix="", length=20, excludes="", symbols=string.printable[:-6]):
    length -= len(prefix)
    symbols = symbols.translate({ord(exclude): None for exclude in excludes})
    return prefix + ''.join(secrets.choice(symbols) for _ in range(length))
