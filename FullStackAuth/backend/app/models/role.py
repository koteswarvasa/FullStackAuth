from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Identity,
    String,
    text
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Role(Base):

    __tablename__ = "ROLE"

    __table_args__ = {
        "schema": "APP"
    }

    role_id: Mapped[int] = mapped_column(
        "ROLE_ID",
        BigInteger,
        Identity(start=1, increment=1),
        primary_key=True
    )

    role_nm: Mapped[str] = mapped_column(
        "ROLE_NM",
        String(100),
        nullable=False,
        unique=True
    )

    role_desc: Mapped[str | None] = mapped_column(
        "ROLE_DESC",
        String(500),
        nullable=True
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