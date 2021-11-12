from pydantic import BaseModel, constr


class TaskApartment(BaseModel):
    id: int


class TaskRoom(BaseModel):
    id: int


class Task(BaseModel):
    id: int
    name: str
    description: str
    apartment: TaskApartment
    points: int
    rooms: list[TaskRoom]
    is_archived: bool


class CreateTask(BaseModel):
    name: constr(max_length=32)  # type: ignore
    description: constr(max_length=128)  # type: ignore
    apartment: int
    rooms: list[int]
    points: int


class UpdateTask(BaseModel):
    name: constr(max_length=32)  # type: ignore
    description: constr(max_length=128)  # type: ignore
    apartment: int
    rooms: list[int]
    points: int
    is_archived: bool
