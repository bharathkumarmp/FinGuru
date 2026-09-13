from pydantic import BaseModel


class LoginRequest(BaseModel):
    mobile: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    mobile: str
    role: str

    class Config:
        from_attributes = True