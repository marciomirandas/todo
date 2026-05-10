from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreateSchema, TaskResponseSchema
from api.deps import get_db, get_current_user
from models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponseSchema)
async def create_task(
    task: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_task = Task(**task.dict(), owner_id=int(user.id))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}")
async def update_task(task_id: int, task: TaskCreateSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    return {"message": "Deleted"}


@router.get("/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/", response_model=list[TaskResponseSchema])
async def get_tasks(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.query(Task).filter(Task.owner_id == int(user.id)).all()
