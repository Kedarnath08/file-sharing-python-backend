from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, JSONResponse
from app.db.models.file import UploadedFiles

async def download_files(
    file_id: str,
    db: Session
    # credentials: HTTPAuthorizationCredentials = Security(token)
):
    record = db.query(UploadedFiles).filter_by(file_id=file_id).first()
    if not record:
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(record.file_path, filename=record.file_name)
