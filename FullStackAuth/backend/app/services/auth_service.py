
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

from app.models.user import User

from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.user_session_repository import UserSessionRepository
from datetime import datetime, timedelta, timezone

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest
)

from app.security.jwt import create_access_token
from app.schemas.auth import LoginResponse

from app.security.password import (
    hash_password,
    verify_password
)

from app.security.refresh_token import (
    generate_refresh_token,
    hash_refresh_token,
)

from fastapi import HTTPException
from app.schemas.auth import LoginResponse

class AuthService:

    def __init__(self, db: Session):

        self.db = db

        self.user_repository = UserRepository(db)

        self.role_repository = RoleRepository(db)

        self.user_role_repository = UserRoleRepository(db)

        self.user_session_repository = UserSessionRepository(db)

    # ==========================================================
    # REGISTER USER
    # ==========================================================

    def register_user(
        self,
        request: RegisterRequest
    ) -> User:

        try:

            # --------------------------------------------------
            # 1. Check whether username already exists
            # --------------------------------------------------

            existing_user = (
                self.user_repository.find_by_username(
                    request.username
                )
            )

            if existing_user is not None:
                raise ValueError(
                    "Username already exists"
                )

            # --------------------------------------------------
            # 2. Check whether email already exists
            # --------------------------------------------------

            existing_user = (
                self.user_repository.find_by_email(
                    request.email
                )
            )

            if existing_user is not None:
                raise ValueError(
                    "Email already exists"
                )

            # --------------------------------------------------
            # 3. Hash password
            # --------------------------------------------------

            password_hash = hash_password(
                request.password
            )

            # --------------------------------------------------
            # 4. Create User entity
            # --------------------------------------------------

            user = User(
                username=request.username,
                email=str(request.email),
                password_hash=password_hash,
                first_nm=request.first_nm,
                last_nm=request.last_nm,
                is_active=True,
                created_by="SYSTEM"
            )

            # --------------------------------------------------
            # 5. Save user
            # --------------------------------------------------

            self.user_repository.create(user)

            # --------------------------------------------------
            # 6. Find default USER role
            # --------------------------------------------------

            user_role = (
                self.role_repository.find_by_name(
                    "USER"
                )
            )

            if user_role is None:
                raise ValueError(
                    "Default USER role is not configured"
                )

            # --------------------------------------------------
            # 7. Assign USER role
            # --------------------------------------------------

            self.user_role_repository.create(
                user_id=user.user_id,
                role_id=user_role.role_id,
                created_by="SYSTEM"
            )

            # --------------------------------------------------
            # 8. Commit transaction
            # --------------------------------------------------

            self.db.commit()

            # --------------------------------------------------
            # 9. Refresh user
            # --------------------------------------------------

            self.db.refresh(user)

            return user

        except Exception:

            # --------------------------------------------------
            # Rollback if anything fails
            # --------------------------------------------------

            self.db.rollback()

            raise

    # ==========================================================
    # LOGIN USER
    # ==========================================================

    def login_user(
        self,
        request: LoginRequest,
        ip_address: str | None = None,
        user_agent: str | None = None
    ) -> tuple[LoginResponse, str]:

        try:

            # --------------------------------------------------
            # 1. Find user by username
            # --------------------------------------------------

            user = (
                self.user_repository.find_by_username(
                    request.username
                )
            )

            # --------------------------------------------------
            # 2. User does not exist
            # --------------------------------------------------

            if user is None:
                raise ValueError(
                    "Invalid username or password"
                )

            # --------------------------------------------------
            # 3. Check whether account is active
            # --------------------------------------------------

            if not user.is_active:
                raise ValueError(
                    "Account is inactive"
                )

            # --------------------------------------------------
            # 4. Verify password
            # --------------------------------------------------

            password_valid = verify_password(
                request.password,
                user.password_hash
            )

            if not password_valid:
                raise ValueError(
                    "Invalid username or password"
                )

            # --------------------------------------------------
            # 5. Get user's active roles
            # --------------------------------------------------

            roles = (
                self.user_role_repository
                .find_active_roles_by_user_id(
                    user.user_id
                )
            )

            # --------------------------------------------------
            # 6. User must have at least one active role
            # --------------------------------------------------

            if not roles:
                raise ValueError(
                    "User has no active role"
                )

            # --------------------------------------------------
            # 7. Current UTC timestamp
            # --------------------------------------------------

            now = datetime.utcnow()

            # --------------------------------------------------
            # 8. Calculate session expiration
            #
            # Access token = 15 minutes
            # Session       = 7 days
            # --------------------------------------------------

            session_expires_at = (
                now
                + timedelta(
                    days=REFRESH_TOKEN_EXPIRE_DAYS
                )
            )

            # --------------------------------------------------
            # 9. Create USER_SESSION
            # --------------------------------------------------

            user_session = (
                self.user_session_repository.create(
                    user_id=user.user_id,
                    expires_tstmp=session_expires_at,
                    created_by=str(user.user_id),
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            )

            # --------------------------------------------------
            # 10. Update LAST_LOGIN_TSTMP
            # --------------------------------------------------

            self.user_repository.update_last_login(
                user,
                now
            )

            refresh_token = generate_refresh_token()

            refresh_token_hash = hash_refresh_token(
                refresh_token
            )

            self.user_session_repository.set_refresh_token_hash(
                user_session=user_session,
                refresh_token_hash=refresh_token_hash,
            )

            # --------------------------------------------------
            # 11. Create access token
            # --------------------------------------------------

            access_token = create_access_token(
                user_id=user.user_id,
                session_id=user_session.session_id,
                roles=roles
            )

            # --------------------------------------------------
            # 12. Commit transaction
            # --------------------------------------------------

            self.db.commit()

            # --------------------------------------------------
            # 13. Return login response
            # --------------------------------------------------

            return LoginResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ), refresh_token

        except Exception:

            # --------------------------------------------------
            # Rollback if anything fails
            # --------------------------------------------------

            self.db.rollback()

            raise
    
def refresh_access_token(self, refresh_token: str):
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or expired refresh session",
    )

    if not refresh_token:
        raise unauthorized

    try:
        old_hash = hash_refresh_token(refresh_token)

        user_session = (
            self.user_session_repository
            .find_by_refresh_token_hash(old_hash)
        )

        if user_session is None:
            raise unauthorized

        now = datetime.now(timezone.utc)
        expires_at = user_session.expires_tstmp

        # SQL Server DATETIME2 values may be timezone-naive.
        if expires_at.tzinfo is not None:
            expires_at = expires_at.astimezone(
                timezone.utc
            ).replace(tzinfo=None)

        now_naive = now.replace(tzinfo=None)

        if (
            user_session.session_status_cd != "ACTIVE"
            or expires_at <= now_naive
        ):
            raise unauthorized

        user = self.user_repository.find_by_id(
            user_session.user_id
        )

        if user is None or not user.is_active:
            raise unauthorized

        roles = self.user_role_repository.get_active_role_names(
            user.user_id
        )

        # Rotate the refresh token so the old one cannot be reused.
        new_refresh_token = generate_refresh_token()
        new_refresh_hash = hash_refresh_token(
            new_refresh_token
        )

        self.user_session_repository.set_refresh_token_hash(
            user_session=user_session,
            refresh_token_hash=new_refresh_hash,
        )

        access_token = create_access_token(
            user_id=user.user_id,
            session_id=user_session.session_id,
            roles=roles,
        )

        self.db.commit()

        return (
            LoginResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ),
            new_refresh_token,
        )

    except HTTPException:
        self.db.rollback()
        raise
    except Exception:
        self.db.rollback()
        raise

