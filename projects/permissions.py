from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

from projects.models import Membership

from .models import Membership


def get_project_or_404(user, project_id, roles=None):
    membership = get_object_or_404(
        Membership.objects.select_related("project"), project_id=project_id, user=user
    )
    if roles and membership.role not in roles:
        raise HttpError(403, f"This needs the {' or '.join(roles)} role")
    return membership.project
