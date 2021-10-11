from fastapi_users import models


class User(models.BaseUser):
    name: str


class UserRegister(models.BaseUserCreate):
    name: str


class UserUpdate(models.BaseUserUpdate):
    name: str


class UserDB(models.BaseUserDB):
    name: str
