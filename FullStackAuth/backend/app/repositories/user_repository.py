from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_username(
        self,
        username: str
    ) -> User | None:

        statement = (
            select(User)
            .where(
                User.username == username
            )
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def find_by_email(
        self,
        email: str
    ) -> User | None:

        statement = (
            select(User)
            .where(
                User.email == email
            )
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()

    def create(
        self,
        user: User
    ) -> User:

        self.db.add(user)

        self.db.flush()

        return user

    def update_last_login(
        self,
        user: User,
        login_tstmp: datetime
    ) -> User:

        user.last_login_tstmp = login_tstmp

        self.db.flush()

        return user
    
    def find_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.user_id == user_id)
        return self.db.execute(statement).scalar_one_or_none()
