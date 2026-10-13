
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    # Find user by username
    def find_by_username(
        self,
        username: str
    ) -> User | None:

        statement = (
            select(User)
            .where(User.username == username)
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    # Find user by email
    def find_by_email(
        self,
        email: str
    ) -> User | None:

        statement = (
            select(User)
            .where(User.email == email)
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    # Create a new user
    def create(
        self,
        user: User
    ) -> User:

        self.db.add(user)
        self.db.flush()

        return user

    # Update last login timestamp
    def update_last_login(
        self,
        user: User,
        login_tstmp: datetime
    ) -> User:

        user.last_login_tstmp = login_tstmp
        self.db.flush()

        return user

    # Find user by ID
    def find_by_id(
        self,
        user_id: int
    ) -> User | None:

        statement = (
            select(User)
            .where(User.user_id == user_id)
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    # Save password reset OTP hash and expiry
    def set_password_reset_otp(
        self,
        user: User,
        otp_hash: str,
        expires_at: datetime
    ) -> None:

        user.password_reset_otp_hash = otp_hash
        user.password_reset_otp_expires_tstmp = expires_at
        user.password_reset_otp_attempts = 0

        self.db.flush()

    # Increment failed OTP attempts
    def increment_password_reset_attempts(
        self,
        user: User
    ) -> int:

        user.password_reset_otp_attempts += 1

        self.db.flush()

        return user.password_reset_otp_attempts

    # Clear password reset OTP details
    def clear_password_reset_otp(
        self,
        user: User
    ) -> None:

        user.password_reset_otp_hash = None
        user.password_reset_otp_expires_tstmp = None
        user.password_reset_otp_attempts = 0

        self.db.flush()

    # Update password and invalidate OTP
    def complete_password_reset(
        self,
        user: User,
        new_password_hash: str
    ) -> None:

        user.password_hash = new_password_hash

        user.password_reset_otp_hash = None
        user.password_reset_otp_expires_tstmp = None
        user.password_reset_otp_attempts = 0

        self.db.flush()
