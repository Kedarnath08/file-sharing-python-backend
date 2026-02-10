from sqlalchemy.orm import Session
from app.db.models.file import SharedFiles, UploadedFiles
from app.db.models.user import User
import uuid

async def send_file(
        file_id: str,
        sender_id:int,
        receiver_id: str,
        db: Session
        
):
    """
    Docstring for share_file
    """
    share_id = str(uuid.uuid4())

    db.add(SharedFiles(
        id=share_id,
        file_id=file_id,
        sender_id=sender_id,
        receiver_id=receiver_id
    ))
    db.commit()

    return {"status": "file shared"}   

async def get_shared_files_list(user_id: int, db: Session):
    # Logic to retrieve shared files for the user
    shared_files = (
        db.query(
            SharedFiles.id,
            SharedFiles.shared_time,
            SharedFiles.receiver_id,
            SharedFiles.file_id,
            SharedFiles.sender_id,
            UploadedFiles.file_name,
            UploadedFiles.file_type,
            User.username.label("sender_username")
        )
        .join(UploadedFiles, SharedFiles.file_id == UploadedFiles.file_id)
        .join(User, SharedFiles.sender_id == User.id)
        .filter(SharedFiles.receiver_id == user_id)
        .all()
    )

    response = []
    for row in shared_files:
        response.append({
            "id": row.id,
            "shared_time": row.shared_time,
            "receiver_id": row.receiver_id,
            "file_id": row.file_id,
            "sender_id": row.sender_id,
            "file_name": row.file_name,
            "file_type": row.file_type,
            "sender_username": row.sender_username,
        })

    return response