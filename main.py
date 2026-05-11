from fastapi import FastAPI
from api.routes import main, auth, tasks

app = FastAPI()

app.include_router(main.router)
app.include_router(auth.router)
app.include_router(tasks.router)
