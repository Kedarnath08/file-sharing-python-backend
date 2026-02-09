from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.config import UPLOAD_DIR
from app.db.models.file import UploadedFiles
import os, uuid

os.makedirs(UPLOAD_DIR, exist_ok=True)

def readable_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


async def store_file(
        file: UploadFile,
        db: Session,
        user_id:int
):
    """
    Docstring for store_file
    """
    file_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    owner_id = user_id
    file_size = str(os.path.getsize(path))
    file_type = file.filename.split(".")[-1] if "." in file.filename else "unknown"

    db.add(UploadedFiles(
        file_id=file_id,
        owner_id=owner_id,
        file_path=path,
        file_name=file.filename,
        file_size=file_size,
        file_type=file_type
        )
    )
    db.commit()

    return {"status": "file uploaded", "file_id": file_id}

async def get_uploaded_files_list(user_id: int, db: Session):
    # Logic to retrieve uploaded files for the user
    files = db.query(UploadedFiles).filter(UploadedFiles.owner_id == user_id).all()
    return files

async def get_uploaded_file_details(file_id: str, user_id: int, db: Session):
    # Logic to retrieve file details
    file_details = db.query(UploadedFiles).filter(UploadedFiles.file_id == file_id).first()
    if not file_details:
            return JSONResponse(status_code=404, content={"error": "File not found"})
    
    return {
        "file_id": file_details.file_id,
        "file_name": file_details.file_name,
        "file_path": file_details.file_path,
        "file_size": readable_size(int(file_details.file_size)) if file_details.file_size.isdigit() else file_details.file_size,
        "file_type": file_details.file_name.split(".")[-1] if "." in file_details.file_name else "unknown",
        "uploaded_by": file_details.owner_id,
        "uploaded_at": file_details.upload_time.isoformat()
    }