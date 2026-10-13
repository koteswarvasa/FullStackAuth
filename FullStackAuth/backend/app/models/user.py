from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Identity,
    String,
    text,
    Integer
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):

    __tablename__ = "USER"

    __table_args__ = {
        "schema": "APP"
    }

    user_id: Mapped[int] = mapped_column(
        "USER_ID",
        BigInteger,
        Identity(start=1, increment=1),
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        "USERNAME",
        String(100),
        nullable=False,
        unique=True
    )

    email: Mapped[str] = mapped_column(
        "EMAIL",
        String(255),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        "PASSWORD_HASH",
        String(255),
        nullable=False
    )

    first_nm: Mapped[str | None] = mapped_column(
        "FIRST_NM",
        String(100),
        nullable=True
    )

    last_nm: Mapped[str | None] = mapped_column(
        "LAST_NM",
        String(100),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        "IS_ACTIVE",
        Boolean,
        nullable=False,
        server_default=text("1")
    )

    last_login_tstmp: Mapped[DateTime | None] = mapped_column(
        "LAST_LOGIN_TSTMP",
        DateTime,
        nullable=True
    )

    created_tstmp: Mapped[DateTime] = mapped_column(
        "CREATED_TSTMP",
        DateTime,
        nullable=False,
        server_default=text("SYSDATETIME()")
    )

    created_by: Mapped[str] = mapped_column(
        "CREATED_BY",
        String(100),
        nullable=False
    )

    updated_tstmp: Mapped[DateTime | None] = mapped_column(
        "UPDATED_TSTMP",
        DateTime,
        nullable=True
    )

    updated_by: Mapped[str | None] = mapped_column(
        "UPDATED_BY",
        String(100),
        nullable=True
    )


    password_reset_otp_hash: Mapped[str | None] = mapped_column(
        "PASSWORD_RESET_OTP_HASH",
        String(64),
        nullable=True,
    )

    password_reset_otp_expires_tstmp: Mapped[datetime | None] = mapped_column(
        "PASSWORD_RESET_OTP_EXPIRES_TSTMP",
        DateTime,
        nullable=True,
    )

    password_reset_otp_attempts: Mapped[int] = mapped_column(
        "PASSWORD_RESET_OTP_ATTEMPTS",
        Integer,
        nullable=False,
        default=0,
    )
