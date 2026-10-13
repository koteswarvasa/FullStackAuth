
import hmac
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.security.password import hash_password
from app.security.password_reset import generate_otp, hash_otp
from app.services.email_service import send_password_reset_otp


# India Standard Time: UTC + 05:30
IST = timezone(timedelta(hours=5, minutes=30))


class PasswordResetService:

    @staticmethod
    def request_password_reset(db: Session, email: str) -> None:
        user_repository = UserRepository(db)

        user = user_repository.find_by_email(email)

        if user is None or not user.is_active:
            return

        otp = generate_otp()
        otp_hash = hash_otp(otp)

        # Generate the current time in IST
        now_ist = datetime.now(IST)

        # OTP expires after 5 minutes
        expires_at_ist = now_ist + timedelta(minutes=5)

        # DATETIME2 does not store timezone information.
        # Store the IST clock time without timezone information.
        expires_at_db = expires_at_ist.replace(tzinfo=None)

        print("OTP generated at IST:", now_ist)
        print("OTP expires at IST:", expires_at_ist)
        print("OTP expiry time saved to DB:", expires_at_db)

        try:
            user_repository.set_password_reset_otp(
                user=user,
                otp_hash=otp_hash,
                expires_at=expires_at_db
            )

            db.commit()

        except Exception:
            db.rollback()
            raise

        try:
            send_password_reset_otp(
                recipient_email=user.email,
                otp=otp
            )

        except Exception as exc:
            try:
                user_repository.clear_password_reset_otp(user)
                db.commit()
            except Exception:
                db.rollback()

            raise HTTPException(
                status_code=503,
                detail=(
                    "Unable to send the verification email. "
                    "Please try again later."
                )
            ) from exc

    @staticmethod
    def reset_password(
        db: Session,
        email: str,
        otp: str,
        new_password: str
    ) -> None:

        user_repository = UserRepository(db)
        user_session_repository = UserSessionRepository(db)

        invalid_otp = HTTPException(
            status_code=400,
            detail="Invalid or expired verification code."
        )

        try:
            user = user_repository.find_by_email(email)

            if user is None or not user.is_active:
                raise invalid_otp

            if (
                not user.password_reset_otp_hash
                or not user.password_reset_otp_expires_tstmp
            ):
                raise invalid_otp

            if user.password_reset_otp_attempts >= 5:
                user_repository.clear_password_reset_otp(user)
                db.commit()
                raise invalid_otp

            # Current IST time without timezone information
            now_ist = datetime.now(IST).replace(tzinfo=None)

            # The database timestamp is now treated as IST.
            expires_at_db = user.password_reset_otp_expires_tstmp

            print("Current time IST:", now_ist)
            print("OTP expiry time IST:", expires_at_db)
            print("OTP expired:", expires_at_db <= now_ist)

            # Validate expiry using IST for both timestamps
            if expires_at_db <= now_ist:
                user_repository.clear_password_reset_otp(user)
                db.commit()
                raise invalid_otp

            submitted_otp = str(otp).strip()
            submitted_hash = hash_otp(submitted_otp)

            if not hmac.compare_digest(
                submitted_hash,
                user.password_reset_otp_hash
            ):
                user_repository.increment_password_reset_attempts(user)
                db.commit()
                raise invalid_otp

            new_password_hash = hash_password(new_password)

            user_repository.complete_password_reset(
                user=user,
                new_password_hash=new_password_hash
            )

            user_session_repository.revoke_all_active_sessions(
                user_id=user.user_id,
                updated_by=str(user.user_id)
            )

            db.commit()

        except HTTPException:
            raise

        except Exception:
            db.rollback()
            raise
