from pydantic import BaseModel, EmailStr, Field

class login(BaseModel):
    """Schema for user login requests."""

    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_.-]+$', example="johndoe")
    password: str = Field(..., min_length=8, max_length=20, example="StrongP@ssw0rd")



class create_user(BaseModel):
    """Schema for new user creation requests."""

    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_.-]+$', example="johndoe")
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, max_length=28, example="StrongP@ssw0rd")
    phone_number: str = Field(..., pattern=r'^\+?\d{7,15}$', example="+1234567890")


