from backend.core.enums import UserRole
from backend.core.exceptions import ForbiddenException

def require_role(current_user_role: str, allowed_roles: list[UserRole]):
    """Strict server-side validation of user role."""
    if current_user_role not in [r.value for r in allowed_roles]:
        raise ForbiddenException(
            f"Role '{current_user_role}' is not authorized to perform this operation. Allowed: {[r.value for r in allowed_roles]}"
        )

def require_contractor(role: str):
    require_role(role, [UserRole.CONTRACTOR])

def require_re(role: str):
    require_role(role, [UserRole.RE])

def require_client(role: str):
    require_role(role, [UserRole.CLIENT])

def require_re_or_client(role: str):
    require_role(role, [UserRole.RE, UserRole.CLIENT])

def require_any_role(role: str):
    require_role(role, [UserRole.CONTRACTOR, UserRole.RE, UserRole.CLIENT])
