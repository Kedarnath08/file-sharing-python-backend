from fastapi import APIRouter, Depends, UploadFile, File, Form, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.utils import handle_internal_server_error
from app.services.files.upload_files import store_file

router = APIRouter(prefix="/files", tags=["files"])
token = HTTPBearer()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    # credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        await store_file(
            file=file,
            db=db,
            # credentials=credentials
        )
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/uploaded/{user_id}")
async def get_uploaded_files(
    user_id: str,
    db: Session = Depends(get_db),
    # credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        # Logic to retrieve uploaded files for the user
        pass
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.post("/share")
async def share_file(
    file_id: str = Form(...),
    receiver_id: str = Form(...),
    db: Session = Depends(get_db),
    # credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        # Logic to share the file with another user
        pass
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/inbox")
async def get_shared_files(
    user_id: str,
    db: Session = Depends(get_db),
    # credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        # Logic to retrieve files shared with the user
        pass
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/download/{file_id}")
async def download_file(
    file_id: str,
    db: Session = Depends(get_db),
    # credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        # Logic to download the file
        pass
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)

