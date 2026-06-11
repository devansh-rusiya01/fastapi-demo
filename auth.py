from fastapi import APIRouter, HTTPException
from models import UserIn
from database import user_collection
from utils import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/signup")
def signup(user: UserIn):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    user_dict = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)
    }
    user_collection.insert_one(user_dict)
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserIn):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token({"user_id": str(db_user["_id"])})
    return {"token": token}

@router.get("/get/devansh")
def get_devansh():
    return {"message": "Hello, Devansh!"}
