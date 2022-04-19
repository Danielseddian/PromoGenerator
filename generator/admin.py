from django.contrib import admin

from models import Group, Promo


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    shown_fields = ("id", "name")
    list_display = shown_fields
    list_editable = ("name",)
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    shown_fields = ("id", "group", "promo")
    list_display = shown_fields
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"
