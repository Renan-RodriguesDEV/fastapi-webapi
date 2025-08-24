from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str


class UserSchemaList(BaseModel):
    status: int
    users: List[UserSchemaPublic]
