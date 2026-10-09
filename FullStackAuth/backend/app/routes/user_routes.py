
from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.security.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
