from pydantic import BaseModel

class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None


class TaskResponseSchema(TaskCreateSchema):
    id: int
    completed: bool

    class Config:
        orm_mode = True


class PaginatedTasksSchema(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[TaskResponseSchema]
