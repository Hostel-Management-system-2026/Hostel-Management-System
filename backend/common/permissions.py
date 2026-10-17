from rest_framework.permissions import BasePermission, IsAuthenticated


def _role_names(request):
    """The user's database role is the only source of truth.

    The JWT "role" claim is for the frontend only and is never trusted here, so a
    token issued before a role change cannot keep the old access.
    """
    role = getattr(request.user, "role", None)
    return {str(role).strip().upper()} if role else set()


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


class IsStudentOrWarden(HasAnyRole):
    allowed_roles = frozenset({"STUDENT", "WARDEN"})
