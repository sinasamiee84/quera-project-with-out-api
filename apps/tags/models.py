from django.db import models
from apps.workspaces.models import Workspace
from core.models.base import TimestampedModel
from core.models.base import SoftDeleteManager, SoftDeleteQuerySet


class TagQuerySet(SoftDeleteQuerySet):
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


class Tag(TimestampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=20, default='#64748b')

    objects = SoftDeleteManager.from_queryset(TagQuerySet)()

    class Meta:
        ordering = ['name']
        constraints = [models.UniqueConstraint(
            fields=['name', 'workspace'],
            name='unique_tag_name_per_workspace',
            condition=models.Q(is_deleted=False)
        )]

    def __str__(self):
        return self.name
