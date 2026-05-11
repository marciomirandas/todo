from fastapi import FastAPI, APIRouter, Depends, HTTPException

router = APIRouter(prefix="", tags=["main"])

@router.get("/")
def read_root():
    return {"message": "API running!"}