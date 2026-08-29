from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.users import User
from app.repositories import users as user_repository
from app.schemas.users import UserCreate


class UserAlreadyExistsError(Exception):
    pass


def register_user( db: Session, user_data: UserCreate) -> User:

    existing_email = user_repository.get_user_by_email(
        db=db,
        email=str(user_data.email),
    )

    if existing_email is not None:
        raise UserAlreadyExistsError(
            "A user with this email already exists."
        )

    existing_username = user_repository.get_user_by_username(
        db=db,
        username=user_data.username,
    )

    if existing_username is not None:
        raise UserAlreadyExistsError(
            "A user with this username already exists."
        )

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        username=user_data.username,
        email=str(user_data.email),
        hashed_password=hashed_password,
    )

    created_user = user_repository.create_user(
        db=db,
        user=user,
    )

    db.commit()
    db.refresh(created_user)

    return created_user

def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = user_repository.get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        return None


    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None


    return user