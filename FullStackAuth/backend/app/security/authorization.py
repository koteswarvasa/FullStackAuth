
from fastapi import Depends, HTTPException, status

from app.security.dependencies import get_current_user
from app.models.user import User


def require_role(required_role: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        # Replace this check with your project's
        # active-role repository lookup if needed.
        user_roles = getattr(current_user, "roles", [])

        if required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_user

    return role_checker
