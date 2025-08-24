from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str


class UserSchemaPatch(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


class UserSchemaList(BaseModel):
    status: int
    users: List[UserSchemaPublic]
