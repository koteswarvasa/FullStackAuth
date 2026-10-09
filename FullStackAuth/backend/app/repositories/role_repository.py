from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_name(self, role_name: str):
        statement = (
            select(Role)
            .where(
                Role.role_nm == role_name,
                Role.is_active == True
            )
        )

        return self.db.execute(
            statement
        ).scalar_one_or_none()