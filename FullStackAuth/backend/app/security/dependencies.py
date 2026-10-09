
from datetime import datetime, timezone
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.security.jwt import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication session",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)

        user_id = int(payload["sub"])
        session_id = UUID(payload["session_id"])

    except Exception:
        raise unauthorized

    user_repository = UserRepository(db)
    session_repository = UserSessionRepository(db)

    user = user_repository.find_by_id(user_id)
    user_session = session_repository.find_by_session_id(session_id)

    if user is None or not user.is_active:
        raise unauthorized

    if user_session is None:
        raise unauthorized

    if user_session.user_id != user_id:
        raise unauthorized

    if user_session.session_status_cd != "ACTIVE":
        raise unauthorized

    # SQL Server DATETIME2 values are normally timezone-naive.
    expires_at = user_session.expires_tstmp

    if expires_at.tzinfo is not None:
        expires_at = expires_at.astimezone(timezone.utc).replace(
            tzinfo=None
        )

    if expires_at <= datetime.now(timezone.utc).replace(tzinfo=None):
        raise unauthorized

    return user
