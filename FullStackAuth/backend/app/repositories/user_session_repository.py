
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user_session import UserSession


class UserSessionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        expires_tstmp: datetime,
        created_by: str,
        ip_address: str | None = None,
        user_agent: str | None = None
    ) -> UserSession:

        user_session = UserSession(
            user_id=user_id,
            expires_tstmp=expires_tstmp,
            ip_address_txt=ip_address,
            user_agent_txt=user_agent,
            created_by=created_by
        )

        self.db.add(user_session)
        self.db.flush()

        return user_session

    def find_by_session_id(
        self,
        session_id: UUID
    ) -> UserSession | None:

        statement = (
            select(UserSession)
            .where(
                UserSession.session_id == session_id
            )
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def update_session_status(
        self,
        user_session: UserSession,
        status_code: str,
        updated_by: str
    ) -> UserSession:

        user_session.session_status_cd = status_code
        user_session.updated_tstmp = datetime.now()
        user_session.updated_by = updated_by

        if status_code == "LOGGED_OUT":
            user_session.logout_tstmp = datetime.now()

        self.db.flush()

        return user_session
    
    def set_refresh_token_hash(
    self,
    user_session: UserSession,
    refresh_token_hash: str
    ) -> UserSession:
        user_session.refresh_token_hash = refresh_token_hash

        self.db.flush()

        return user_session

    
    def find_by_refresh_token_hash(
        self, refresh_token_hash: str
    ) -> UserSession | None:
        statement = select(UserSession).where(
            UserSession.refresh_token_hash == refresh_token_hash
        )
        return self.db.execute(statement).scalar_one_or_none()

