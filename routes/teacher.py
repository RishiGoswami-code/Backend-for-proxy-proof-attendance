from fastapi import APIRouter, HTTPException, Depends, status
from models.teacher_model import TeacherCreateModel, TeacherResponseModel
from models.attendance_model import AttendanceResponseModel
from database.mongo import AsyncDatabase
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from .auth import get_current_active_user
from models.student_model import StudentResponseModel

router = APIRouter()

def get_db():
    return AsyncDatabase.get_db()

@router.post("/", response_model=TeacherResponseModel, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: TeacherCreateModel, db: AsyncIOMotorDatabase = Depends(get_db)):
    teacher_dict = teacher.model_dump(by_alias=True)
    teacher_dict["created_at"] = datetime.utcnow()
    teacher_dict["is_active"] = True
    teacher_dict["device_token"] = None

    result = await db["teachers"].insert_one(teacher_dict)

    if result.inserted_id:
        new_teacher = await db["teachers"].find_one({"_id": result.inserted_id})
        return TeacherResponseModel(**new_teacher)

    raise HTTPException(status_code=500, detail="Failed to create teacher")


@router.get("/", response_model=List[TeacherResponseModel])
async def get_all_teachers(db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    teachers = []
    async for teacher in db["teachers"].find():
        teachers.append(TeacherResponseModel(**teacher))
    return teachers


@router.get("/{teacher_id}", response_model=TeacherResponseModel)
async def get_teacher(teacher_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    
    teacher = await db["teachers"].find_one({"_id": ObjectId(teacher_id)})
    
    if teacher:
        return TeacherResponseModel(**teacher)
    
    raise HTTPException(status_code=404, detail="Teacher not found")

@router.post("/{teacher_id}/device-token")
async def update_device_token(teacher_id: str, token: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

    update_result = await db["teachers"].update_one(
        {"_id": ObjectId(teacher_id)},
        {"$set": {"device_token": token}}
    )

    if update_result.modified_count == 1:
        return {"message": "Device token updated successfully"}

    raise HTTPException(status_code=404, detail="Teacher not found or token already updated")


@router.get("/my-classes", response_model=List[str])
async def get_my_classes(current_user: TeacherResponseModel = Depends(get_current_active_user)):
    """Returns the list of batches/classes assigned to the current teacher."""
    return current_user.batches


@router.get("/my-subjects", response_model=List[str])
async def get_my_subjects(current_user: TeacherResponseModel = Depends(get_current_active_user)):
    """Returns the list of subjects assigned to the current teacher."""
    return current_user.subjects


@router.get("/class-attendance/{class_id}", response_model=List[AttendanceResponseModel])
async def get_attendance_by_class(
    class_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: TeacherResponseModel = Depends(get_current_active_user)
):
    """
    Teacher endpoint to view attendance records for a specific class.
    Ensures the teacher is authorized to view the class.
    """
    if class_id not in current_user.batches:
        raise HTTPException(status_code=403, detail="You are not authorized to view this class's attendance.")
    
    attendance_records = []
    async for record in db["attendance"].find({"class_id": class_id}):
        attendance_records.append(AttendanceResponseModel(**record))
    
    return attendance_records


@router.get("/class-students/{class_id}", response_model=List[StudentResponseModel])
async def get_students_by_class(
    class_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: TeacherResponseModel = Depends(get_current_active_user)
):
    """
    Teacher endpoint to view the list of students in a specific class.
    Ensures the teacher is authorized to view the class.
    """
    if class_id not in current_user.batches:
        raise HTTPException(status_code=403, detail="You are not authorized to view this class's students.")

    students = []
    async for student in db["students"].find({"batch": class_id}):
        students.append(StudentResponseModel(**student))

    return students

