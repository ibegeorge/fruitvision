from sqlalchemy.orm import Session

from app.models.predictions import Prediction


def create_prediction(
    db: Session,
    *,
    user_id: int,
    image_path: str,
    predicted_class: str,
    confidence: float,
) -> Prediction:
    """
    Create and store a prediction record.
    """

    prediction = Prediction(
        user_id=user_id,
        image_path=image_path,
        predicted_class=predicted_class,
        confidence=confidence,
    )

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    return prediction



def get_predictions_by_user(
    db: Session,
    user_id: int,
) -> list[Prediction]:
    """
    Retrieve all predictions belonging to a user.
    """

    return (
        db.query(Prediction)
        .filter(
            Prediction.user_id == user_id
        )
        .all()
    )