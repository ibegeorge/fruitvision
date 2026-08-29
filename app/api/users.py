from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.models.users import User
from app.schemas.users import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ],
):
    return current_user