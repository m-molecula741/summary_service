from uuid import UUID

from pydantic import EmailStr

from app.core.base_schemas import ObjSchema


class User(ObjSchema):
    id: UUID
    nickname: str
    email: EmailStr
    is_superuser: bool


class AuthSchema(ObjSchema):
    scheme: str
    credentials: str
