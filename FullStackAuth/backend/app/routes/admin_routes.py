
from fastapi import APIRouter, Depends

from app.models.user import User
from app.security.authorization import require_role

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_role("ADMIN")),
):
    return {
        "message": "Welcome to the admin dashboard",
        "user_id": current_user.user_id,
    }
