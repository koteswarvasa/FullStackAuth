from pydantic import BaseModel, EmailStr, Field, model_validator


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



class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(pattern=r"^[0-9]{6}$")


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(pattern=r"^[0-9]{6}$")
    new_password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
