from pydantic import BaseModel

class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None

class TaskResponseSchema(TaskCreateSchema):
    id: int
    completed: bool

    class Config:
        orm_mode = True