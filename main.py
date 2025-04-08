from fastapi import FastAPI
from auth import router as auth_router
from task import router as task_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)
