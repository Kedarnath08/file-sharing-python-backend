from fastapi import APIRouter, Depends, UploadFile, File, Form, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.utils import handle_internal_server_error
from app.services.files.upload_files import store_file, get_uploaded_files_list, get_uploaded_file_details
from app.services.files.share_files import send_file, get_shared_files_list
from app.services.files.download import download_files
from app.services.users.user_functions import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/files", tags=["files"])
token = HTTPBearer()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        response = await store_file(
            file=file,
            db=db,
            user_id=current_user.id,
        )
        return response
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/uploaded")
async def get_uploaded_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        response = await get_uploaded_files_list(user_id=current_user.id, db=db)
        return response
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/details/{file_id}")
async def get_file_details(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        response = await get_uploaded_file_details(file_id=file_id, user_id=current_user.id, db=db)
        return response
        
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as exc :
        handle_internal_server_error(exc)


@router.post("/share")
async def share_file(
    file_id: str = Form(...),
    receiver_id: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        response = await send_file(
            file_id=file_id,
            sender_id=current_user.id,
            receiver_id=receiver_id,
            db=db
        )
        return response
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/inbox")
async def get_shared_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        response = await get_shared_files_list(user_id=current_user.id, db=db)
        return response
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)


@router.get("/download/{file_id}")
async def download_file(
    file_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(token)
):
    try:
        response = await download_files(file_id=file_id, db=db)
        return response
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc :
        handle_internal_server_error(exc)

