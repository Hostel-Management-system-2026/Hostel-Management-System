from rest_framework.permissions import BasePermission, IsAuthenticated


def _role_names(request):
    """Read the role exposed by the shared authentication layer."""
    user = request.user
    values = [getattr(user, "role", None)]

    token = request.auth
    if isinstance(token, dict):
        values.append(token.get("role"))
    elif token is not None:
        values.append(getattr(token, "role", None))

    groups = getattr(user, "groups", None)
    if groups is not None:
        values.extend(groups.values_list("name", flat=True))

    return {str(value).strip().upper().removeprefix("ROLE_") for value in values if value}


class HasAnyRole(BasePermission):
    allowed_roles = frozenset()

    def has_permission(self, request, view):
        if not IsAuthenticated().has_permission(request, view):
            return False
        return bool(_role_names(request) & self.allowed_roles)


class IsWarden(HasAnyRole):
    allowed_roles = frozenset({"WARDEN"})


class IsAdmin(HasAnyRole):
    allowed_roles = frozenset({"ADMIN"})


class IsStudent(HasAnyRole):
    allowed_roles = frozenset({"STUDENT"})


class IsStudentOrWardenOrAdmin(HasAnyRole):
    allowed_roles = frozenset({"STUDENT", "WARDEN", "ADMIN"})
