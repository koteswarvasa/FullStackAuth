from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user_role import UserRole


class UserRoleRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        role_id: int,
        created_by: str
    ) -> UserRole:

        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            created_by=created_by,
            is_active=True
        )

        self.db.add(user_role)
        self.db.flush()

        return user_role

    def find_active_roles_by_user_id(
    self,
    user_id: int
    ) -> list[str]:

        statement = (
            select(Role.role_nm)
            .join(
                UserRole,
                UserRole.role_id == Role.role_id
            )
            .where(
                UserRole.user_id == user_id,
                UserRole.is_active == True,
                Role.is_active == True
            )
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())