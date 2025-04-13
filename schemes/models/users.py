from pydantic import BaseModel


class UserCreateScheme(BaseModel):
    id: int


class UserDTO(UserCreateScheme):
    pass
