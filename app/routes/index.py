from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
router = APIRouter()
@router.get("/login")
def login():
    print("hello api called");
    return "hello"