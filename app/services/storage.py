from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


def save_image(file: UploadFile) -> str:
    """
    Save uploaded image locally and return the stored path.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported image format"
        )

    unique_filename = (
        f"{uuid4().hex}{extension}"
    )

    file_path = UPLOAD_DIR / unique_filename


    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())


    return str(file_path)