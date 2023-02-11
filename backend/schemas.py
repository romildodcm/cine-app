from pydantic import BaseModel
from sqlalchemy.orm import Session

class UserModel(BaseModel):
    email: str
    name: str
    password: str
    email: str

class UserCreate(UserModel):
    password: str

class User(UserModel):
    id: int
    class Config:
        orm_mode = True

class UserUpdate(UserModel):
    name: str
    email: str
    password: str

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
