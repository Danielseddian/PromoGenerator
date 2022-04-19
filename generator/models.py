from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ("id",)

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"


class Promo(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    promo = models.CharField(unique=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ("id", "group")

    def __str__(self):
        return f"id: {self.id}, promo: {self.promo}, group: {self.group}"
