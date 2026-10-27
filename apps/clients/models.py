from django.db import models
from apps.workspaces.models import Workspace
from core.models.base import TimestampedModel
from core.models.base import SoftDeleteManager ,SoftDeleteQuerySet

class ClientQuerySet(SoftDeleteQuerySet):

    def visible_to(self, user):

        if not user or not user.is_authenticated:
            return self.none()

        return self.filter(
            workspace__memberships__user=user,
            workspace__memberships__is_active=True,
            workspace__memberships__is_deleted=False,
            is_deleted=False
        ).distinct()



class Client(TimestampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField( blank=True)
    thumbnail = models.ImageField(upload_to='clients/', null=True, blank=True)

    objects = SoftDeleteManager.from_queryset(ClientQuerySet)()

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'workspace'],
                name='unique_client_name_per_workspace',
                condition=models.Q(is_deleted=False)
            )
        ]

    def __str__(self):
        return self.name
