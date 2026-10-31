from rest_framework.permissions import BasePermission, IsAuthenticated


def _role_names(request):
    """Use only the role loaded on the authenticated database user."""
    role = getattr(request.user, "role", None)
    return {role} if isinstance(role, str) and role else set()


class HasAnyRole(BasePermission):
    allowed_roles = frozenset()

    def has_permission(self, request, view):
        if not IsAuthenticated().has_permission(request, view):
            return False
        return bool(_role_names(request) & self.allowed_roles)


class IsWarden(HasAnyRole):
    allowed_roles = frozenset({"WARDEN"})
    
class IsWardenOrAdmin(HasAnyRole):
    allowed_roles = frozenset({"WARDEN", "ADMIN"})


class IsAdmin(HasAnyRole):
    allowed_roles = frozenset({"ADMIN"})


class IsStudent(HasAnyRole):
    allowed_roles = frozenset({"STUDENT"})


class IsStudentOrWardenOrAdmin(HasAnyRole):
    allowed_roles = frozenset({"STUDENT", "WARDEN", "ADMIN"})


class IsStudentOrWarden(HasAnyRole):
    allowed_roles = frozenset({"STUDENT", "WARDEN"})
