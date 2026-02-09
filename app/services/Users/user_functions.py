import bcrypt
from app.db.models.user import User
from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from datetime import timedelta

SECRET_KEY = "MOBILE_APP"  # move to env var in real apps
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#function to hash the password
def hash_password(password: str) -> str:
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

async def user_creation(user_data, db):
    # user creation logic 
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": db_user}


async def user_login_function(user_data, db):
    # Find user
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if not db_user:
        raise Exception("User not found")

    # Check password
    if not bcrypt.checkpw(
        user_data.password.encode("utf-8"),
        db_user.hashed_password.encode("utf-8")
    ):
        raise Exception("Invalid credentials")

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.username, "user_id": db_user.id},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    

async def user_logout(db):
    ''' API to logout the user. '''
    try:
        result = db.query(User).filter(User.is_active == True).update({"is_active": False})
        db.commit() 
        return result
    except Exception as e:
        db.rollback()
        raise e