from apps.workspaces.models import WorkspaceMembership

ROLE_RANK = {
    'owner': 3,
    'admin': 2,
    'manager': 2,
    'member': 1,
}


def get_workspace_membership(user, workspace):

    if not user or not user.is_authenticated:
        return None

    return (
        WorkspaceMembership.objects.filter(
            workspace=workspace,
            user=user,
            is_active=True,
            is_deleted=False,
        )
        .first()
    )


def get_workspace_role(user, workspace):

    if not user or not user.is_authenticated:
        return None

    if workspace.owner_id == user.id or workspace.owner == user:
        return 'owner'

    membership = get_workspace_membership(user, workspace)
    if membership:
        return membership.role

    return None


def has_workspace_role(user, workspace, minimum_role):

    role = get_workspace_role(user, workspace)

    if role is None:
        return False

    user_rank = ROLE_RANK.get(role, 0)
    required_rank = ROLE_RANK.get(minimum_role, 0)

    return user_rank >= required_rank
