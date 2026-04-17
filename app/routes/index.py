from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.user.index import UserController
from app.db.session import get_DB
from app.schemas.userSchema import UserCreate

router = APIRouter()
# @router.post("/create")
# def register(data: UserCreate,db: Session = Depends(get_DB)):
#     print("hello api called");
#     return "hello"
@router.get("/")
def main():
  return "hello"
@router.get("/demo")
def demo(db: Session = Depends(get_DB)):
  return UserController().demo(db)