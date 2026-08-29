from sqlalchemy.orm import Session

from app.ai.inference import predict_image
from app.repositories.predictions import create_prediction
from app.services.storage import save_image


def create_user_prediction(
    db: Session,
    *,
    user_id: int,
    image,
):
    """
    Complete prediction workflow.
    """

    image_path = save_image(image)

    result = predict_image(
        image_path
    )

    prediction = create_prediction(
        db=db,
        user_id=user_id,
        image_path=image_path,
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
    )

    return prediction