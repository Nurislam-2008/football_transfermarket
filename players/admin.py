from django.contrib import admin
from django.utils.html import format_html
from .models import Country, Club, Player, Transfer


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded')
    list_filter = ('country',)
    search_fields = ('name',)


class TransferInline(admin.TabularInline):
    model = Transfer
    extra = 1


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'position', 'age', 'club', 'market_value', 'goals')
    list_filter = ('position', 'club', 'nationality')
    search_fields = ('name',)
    list_editable = ('market_value', 'club')
    inlines = [TransferInline]

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'photo', 'number', 'age', 'position', 'nationality', 'club')
        }),
        ('Финансы', {
            'fields': ('market_value',)
        }),
        ('Статистика', {
            'fields': ('matches', 'goals', 'assists')
        }),
        ('Достижения', {
            'fields': ('achievements',)
        }),
    )

    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:40px; width:40px; border-radius:50%; object-fit:cover;" />',
                obj.photo.url
            )
        return '—'


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('player', 'from_club', 'to_club', 'price', 'year')
    list_filter = ('year',)
    search_fields = ('player__name',)