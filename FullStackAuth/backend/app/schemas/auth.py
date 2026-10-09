from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    first_nm: str | None = Field(
        default=None,
        max_length=100
    )

    last_nm: str | None = Field(
        default=None,
        max_length=100
    )


class LoginRequest(BaseModel):

    username: str

    password: str


class LoginResponse(BaseModel):

    access_token: str

    token_type: str

    expires_in: int
