from django.contrib import admin

from .models import Group, Promo, ExtAccess


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    shown_fields = ("id", "group")
    list_display = shown_fields
    list_editable = ("group", )
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    shown_fields = ("id", "group", "promo")
    list_display = shown_fields
    search_fields = shown_fields
    list_display_links = ("id", "group")
    list_editable = ("promo",)
    list_filter = shown_fields
    empty_value_display = "-пусто-"


@admin.register(ExtAccess)
class AccessAdmin(admin.ModelAdmin):
    shown_fields = ("id", "group")
    list_display = shown_fields
    list_editable = ("group", )
    filter_vertical = ("users", )
    search_fields = shown_fields
    list_filter = shown_fields
    empty_value_display = "-пусто-"
