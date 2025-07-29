from fastapi import APIRouter, HTTPException
from models.student_model import StudentCreateModel, StudentResponseModel
from typing import List

router = APIRouter()

# Dummy database
fake_students_db = []

@router.post("/", response_model=StudentResponseModel)
async def create_student(student: StudentCreateModel):
    student_dict = student.dict()
    student_dict["_id"] = "student_id_" + str(len(fake_students_db) + 1)
    student_dict["created_at"] = "2025-07-19T15:29:45"
    student_dict["is_active"] = True
    student_dict["device_token"] = "fcm_token_" + str(len(fake_students_db) + 1)
    fake_students_db.append(student_dict)
    return student_dict

@router.get("/", response_model=List[StudentResponseModel])
async def get_all_students():
    return fake_students_db

@router.get("/{student_id}", response_model=StudentResponseModel)
async def get_student(student_id: str):
    for student in fake_students_db:
        if student["_id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@router.post("/{student_id}/device-token")
async def update_device_token(student_id: str, token: str):
    for student in fake_students_db:
        if student["_id"] == student_id:
            student["device_token"] = token
            return {"message": "Device token updated successfully"}
    raise HTTPException(status_code=404, detail="Student not found")