from uuid import UUID
from sqlalchemy import String

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    String,
    Uuid,
    text
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserSession(Base):

    __tablename__ = "USER_SESSION"

    __table_args__ = {
        "schema": "APP"
    }

    session_id: Mapped[UUID] = mapped_column(
        "SESSION_ID",
        Uuid(as_uuid=True),
        primary_key=True,
        server_default=text("NEWID()")
    )

    user_id: Mapped[int] = mapped_column(
        "USER_ID",
        BigInteger,
        ForeignKey("APP.USER.USER_ID"),
        nullable=False
    )

    login_tstmp: Mapped[DateTime] = mapped_column(
        "LOGIN_TSTMP",
        DateTime,
        nullable=False,
        server_default=text("SYSDATETIME()")
    )

    logout_tstmp: Mapped[DateTime | None] = mapped_column(
        "LOGOUT_TSTMP",
        DateTime,
        nullable=True
    )

    session_status_cd: Mapped[str] = mapped_column(
        "SESSION_STATUS_CD",
        String(20),
        nullable=False,
        server_default=text("'ACTIVE'")
    )

    ip_address_txt: Mapped[str | None] = mapped_column(
        "IP_ADDRESS_TXT",
        String(50),
        nullable=True
    )

    user_agent_txt: Mapped[str | None] = mapped_column(
        "USER_AGENT_TXT",
        String(1000),
        nullable=True
    )

    expires_tstmp: Mapped[DateTime] = mapped_column(
        "EXPIRES_TSTMP",
        DateTime,
        nullable=False
    )
    
    refresh_token_hash: Mapped[str | None] = mapped_column(
    "REFRESH_TOKEN_HASH",
    String(255),
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

