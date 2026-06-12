from fastapi import APIRouter, Depends
from auth_deps import get_current_user
from database import task_collection
from pydantic import BaseModel
from bson import ObjectId

router = APIRouter()

class Task(BaseModel):
    title: str
    description: str

@router.post("/create-task")
def create_task(task: Task, user=Depends(get_current_user)):
    task_dict = {
        "user_id": user["user_id"],
        "title": task.title,
        "description": task.description
    }
    task_collection.insert_one(task_dict)
    return {"msg": "Task created"}

@router.get("/my-tasks")
def get_my_tasks(user=Depends(get_current_user)):
    tasks = list(task_collection.find({"user_id": user["user_id"]}))
    for task in tasks:
        task["_id"] = str(task["_id"])  # Convert ObjectId to string
    return tasks
