from sqlalchemy.orm import Session
from app.db.models.file import SharedFiles
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
    shared_files = db.query(SharedFiles).filter(SharedFiles.receiver_id == user_id).all()
    return shared_files