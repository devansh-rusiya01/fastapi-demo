from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    email: str
    password: str
