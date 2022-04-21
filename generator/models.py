from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    group = models.CharField(max_length=100, unique=True, verbose_name="Группа")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="promo_group")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ("id",)

    def __str__(self):
        return f"id: {self.id}, name: {self.group}"


class Promo(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа", related_name="promo")
    promo = models.CharField(max_length=120, unique=True, verbose_name="Промокод")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ("id", "group")

    def __str__(self):
        return f"id: {self.id}, promo: {self.promo}, group: {self.group}"


class ExtAccess(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа", related_name="access")
    users = models.ManyToManyField(User, related_name="access", blank=True)

    class Meta:
        verbose_name = "Доступ"
        verbose_name_plural = "Доступы"
        ordering = ("id", "group")

    def __str__(self):
        return f"id: {self.id}, group: {self.group}"
