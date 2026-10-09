from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Identity,
    String,
    UniqueConstraint,
    text
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserRole(Base):

    __tablename__ = "USER_ROLE"

    __table_args__ = (
        UniqueConstraint(
            "USER_ID",
            "ROLE_ID",
            name="UQ_USER_ROLE"
        ),
        {
            "schema": "APP"
        }
    )

    user_role_id: Mapped[int] = mapped_column(
        "USER_ROLE_ID",
        BigInteger,
        Identity(start=1, increment=1),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        "USER_ID",
        BigInteger,
        ForeignKey("APP.USER.USER_ID"),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        "ROLE_ID",
        BigInteger,
        ForeignKey("APP.ROLE.ROLE_ID"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        "IS_ACTIVE",
        Boolean,
        nullable=False,
        server_default=text("1")
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