from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.dependencies import get_current_user

from app.models.users import User
from app.schemas.predictions import PredictionResponse, PredictionListResponse

from app.services.predictions import create_user_prediction
from app.repositories.predictions import (
    get_predictions_by_user,
)


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prediction(
    image: UploadFile = File(...),

    current_user: Annotated[
        User,
        Depends(get_current_user)
    ] = None,

    db: Annotated[
        Session,
        Depends(get_db)
    ] = None,
):

    try:

        prediction = create_user_prediction(
            db=db,
            user_id=current_user.id,
            image=image,
        )

        return prediction


    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "",
    response_model=PredictionListResponse,
)
def get_user_predictions(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ],

    db: Annotated[
        Session,
        Depends(get_db)
    ],
):

    predictions = get_predictions_by_user(
        db=db,
        user_id=current_user.id,
    )

    return {
        "predictions": predictions
    }