from fastapi import APIRouter, HTTPException, Depends
from models import UserSignup, UserLogin
from database import user_collection
from utils import hash_password, verify_password, create_token
from dependencies import get_current_user

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    user_dict = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": hash_password(user.password),
        "phone_number": user.phone_number,
        "role": user.role
    }
    user_collection.insert_one(user_dict)
    return {
        "message": "User created successfully",
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role
        }
    }

@router.post("/login")
def login(user: UserLogin):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token, expires_in = create_token({"user_id": str(db_user["_id"])})
    return {
        "token": token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": {
            "first_name": db_user.get("first_name"),
            "last_name": db_user.get("last_name"),
            "email": db_user["email"]
        }
    }

@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Welcome! You are logged in.",
        "user": {
            "first_name": current_user.get("first_name"),
            "last_name": current_user.get("last_name"),
            "email": current_user.get("email"),
            "role": current_user.get("role")
        }
    }
