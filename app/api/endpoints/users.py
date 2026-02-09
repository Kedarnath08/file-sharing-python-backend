from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user_model import login, create_user, UserResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.services.Users.user_functions import user_creation, user_logout, user_login_function, get_current_user

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()

@router.post("/create_user", response_model=UserResponse)
async def create_new_user(user: create_user, db: Session = Depends(get_db)):
    '''Endpoint to create a new user.'''
    try:
        db_user = await user_creation(user,db)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def user_login(user: login, db: Session = Depends(get_db)):
    try:
        result = await user_login_function(user, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/user_profile")
async def get_logged_in_user_profile(
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }



@router.get("/user_list")
async def get_users_list(db: Session = Depends(get_db)):
    return {"message": "User list retrieved successfully"}


@router.post("/logout")
async def logout(db: Session = Depends(get_db)):
    user = await user_logout(db)
    if user == 0:
        raise HTTPException(status_code=400, detail="No active user found to logout")
    return {"status": user, "message": "Logout successful"}


