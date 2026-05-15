from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional


class TaskCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponseSchema(TaskCreateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedTasksSchema(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list[TaskResponseSchema]
