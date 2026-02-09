from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.core.config import UPLOAD_DIR
from app.db.models.file import UploadedFiles
import os, uuid

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def store_file(
        file: UploadFile,
        db: Session
        # credentials: HTTPAuthorizationCredentials
        
):
    """
    Docstring for store_file
    """
    file_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    owner_id = "owner_id_placeholder"  # Replace with actual owner ID retrieval logic

    db.add(UploadedFiles(
        file_id=file_id,
        owner_id=owner_id,
        file_path=path,
        file_name=file.filename
        )
    )
    db.commit()

    return {"status": "file uploaded", "file_id": file_id}