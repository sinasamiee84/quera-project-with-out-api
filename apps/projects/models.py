from django.core.exceptions import ValidationError
from django.db import models

from apps.clients.models import Client
from apps.workspaces.models import Workspace
from core.models.base import (
    SoftDeleteManager,
    SoftDeleteQuerySet,
    TimestampedModel,
)


class ProjectQuerySet(SoftDeleteQuerySet):

    def visible_to(self, user):
        if not user or not user.is_authenticated:
            return self.none()
        return self.filter(
            workspace__memberships__user=user,
            workspace__memberships__is_active=True,
            workspace__memberships__is_deleted=False,
            workspace__is_deleted=False,
            is_deleted=False,
        ).distinct()

    def not_archived(self):
        return self.filter(is_archived=False)


class Project(TimestampedModel):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name='projects'
    )
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=20, default='#2563eb')
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    # پرانتز پایانی الزامی است
    objects = SoftDeleteManager.from_queryset(ProjectQuerySet)()

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'workspace'],
                name='unique_project_name_per_workspace',
                condition=models.Q(is_deleted=False),
            )
        ]

    def clean(self):
        super().clean()
        if self.client and self.workspace:
            if self.client.workspace != self.workspace:
                raise ValidationError(
                    'Client must belong to the same workspace.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

