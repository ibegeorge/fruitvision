from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provide one SQLAlchemy session for the duration of a request.

    The session is always closed after the request finishes, including when
    endpoint execution raises an exception.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


DatabaseSession = Annotated[Session, Depends(get_db)]