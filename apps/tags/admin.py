from django.contrib import admin
from .models import Tag
from core.admins.base import SoftDeleteAdmin


@admin.register(Tag)
class TagAdmin(SoftDeleteAdmin):
    list_display = ('workspace', 'name','color')
    search_fields = ('name',)
    list_filter = ('workspace',)
    ordering = ('-created_at',)

