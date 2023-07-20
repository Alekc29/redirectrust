from django.contrib import admin

from .models import Stat, Connect


class StatAdmin(admin.ModelAdmin):
    list_display = (
        'donater',
        'count_unisender',
        'balance',
        'donat',
    )
    search_fields = ('balance',)
    empty_value_display = '-пусто-'


class ConnectAdmin(admin.ModelAdmin):
    list_display = (
        'donater',
        'feedback',
    )
    search_fields = ('donater',)
    empty_value_display = '-пусто-'


admin.site.register(Stat, StatAdmin)
admin.site.register(Connect, ConnectAdmin)

