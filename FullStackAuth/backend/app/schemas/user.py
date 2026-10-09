from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):

    user_id: int
    username: str
    email: str
    first_nm: str | None = None
    last_nm: str | None = None
    is_active: bool
    last_login_tstmp: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )