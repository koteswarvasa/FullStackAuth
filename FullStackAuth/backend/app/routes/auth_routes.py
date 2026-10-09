
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    Cookie,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config import REFRESH_TOKEN_EXPIRE_DAYS
from app.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.security.dependencies import (
    bearer_scheme,
    get_current_user,
)
from app.security.jwt import decode_access_token
from app.repositories.user_session_repository import (
    UserSessionRepository,
)
from app.models.user import User


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# ============================
# REGISTER
# ============================
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        auth_service = AuthService(db)
        user = auth_service.register_user(request)
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


# ============================
# LOGIN
# ============================
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    request: LoginRequest,
    http_request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    client_ip = (
        http_request.client.host
        if http_request.client
        else None
    )
    user_agent = http_request.headers.get("user-agent")

    auth_service = AuthService(db)

    login_response, refresh_token = auth_service.login_user(
        request=request,
        ip_address=client_ip,
        user_agent=user_agent,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Local HTTP development only
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )

    return login_response


# ============================
# LOGOUT
# ============================
@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
def logout(
    response: Response,
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Decode the validated access token to get the session ID.
        payload = decode_access_token(
            credentials.credentials
        )
        session_id = UUID(payload["session_id"])

        session_repository = UserSessionRepository(db)

        user_session = (
            session_repository.find_by_session_id(session_id)
        )

        if user_session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found",
            )

        if user_session.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session",
            )

        if user_session.session_status_cd != "ACTIVE":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session is already inactive",
            )

        # Revoke the database session.
        session_repository.update_session_status(
            user_session=user_session,
            status_code="LOGGED_OUT",
            updated_by=str(current_user.user_id),
        )

        db.commit()

        # Clear the browser's refresh-token cookie.
        response.delete_cookie(
            key="refresh_token",
            path="/api/v1/auth",
            secure=False,  # Local HTTP development only
            httponly=True,
            samesite="lax",
        )

        return {
            "message": "Logout successful"
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        # Keep this temporarily for local debugging.
        print("LOGOUT ERROR:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to complete logout",
        )


# ============================
# REFRESH ACCESS TOKEN
# ============================
@router.post(
    "/refresh",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)

    login_response, new_refresh_token = (
        auth_service.refresh_access_token(refresh_token)
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  # Local HTTP development only
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )

    return login_response
