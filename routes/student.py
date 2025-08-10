from fastapi import APIRouter, HTTPException, Depends, status
from models.student_model import StudentCreateModel, StudentResponseModel
from typing import List
from database.mongo import AsyncDatabase
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from .auth import get_current_active_user, get_password_hash

router = APIRouter()

def get_db():
    return AsyncDatabase.get_db()


@router.post("/", response_model=StudentResponseModel, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreateModel, db: AsyncIOMotorDatabase = Depends(get_db)):
    # This endpoint is also available to Admins through the /admin/students/ route
    student_dict = student.model_dump(by_alias=True)
    student_dict["created_at"] = datetime.utcnow()
    student_dict["is_active"] = True
    student_dict["password"] = get_password_hash(student_dict["password"])
    student_dict["device_token"] = None

    result = await db["students"].insert_one(student_dict)

    if result.inserted_id:
        new_student = await db["students"].find_one({"_id": result.inserted_id})
        return StudentResponseModel(**new_student)
    
    raise HTTPException(status_code=500, detail="Failed to create student")


@router.get("/", response_model=List[StudentResponseModel])
async def get_all_students(db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    students = []
    async for student in db["students"].find():
        students.append(StudentResponseModel(**student))
    return students


@router.get("/{student_id}", response_model=StudentResponseModel)
async def get_student(student_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    
    student = await db["students"].find_one({"_id": ObjectId(student_id)})
    
    if student:
        return StudentResponseModel(**student)
    
    raise HTTPException(status_code=404, detail="Student not found")


@router.post("/{student_id}/device-token")
async def update_device_token(student_id: str, token: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

    update_result = await db["students"].update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"device_token": token}}
    )

    if update_result.modified_count == 1:
        return {"message": "Device token updated successfully"}
    
    raise HTTPException(status_code=404, detail="Student not found or token already updated")
