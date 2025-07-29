from fastapi import APIRouter, HTTPException
from models.teacher_model import TeacherCreateModel, TeacherResponseModel
from typing import List

router = APIRouter()

# Dummy database
fake_teachers_db = []

@router.post("/", response_model=TeacherResponseModel)
async def create_teacher(teacher: TeacherCreateModel):
    teacher_dict = teacher.dict()
    teacher_dict["_id"] = "teacher_id_" + str(len(fake_teachers_db) + 1)
    teacher_dict["created_at"] = "2025-07-20T23:51:01"
    teacher_dict["is_active"] = True
    teacher_dict["device_token"] = "fcm_token_" + str(len(fake_teachers_db) + 1)
    fake_teachers_db.append(teacher_dict)
    return teacher_dict

@router.get("/", response_model=List[TeacherResponseModel])
async def get_all_teachers():
    return fake_teachers_db

@router.get("/{teacher_id}", response_model=TeacherResponseModel)
async def get_teacher(teacher_id: str):
    for teacher in fake_teachers_db:
        if teacher["_id"] == teacher_id:
            return teacher
    raise HTTPException(status_code=404, detail="Teacher not found")

@router.post("/{teacher_id}/device-token")
async def update_device_token(teacher_id: str, token: str):
    for teacher in fake_teachers_db:
        if teacher["_id"] == teacher_id:
            teacher["device_token"] = token
            return {"message": "Device token updated successfully"}
    raise HTTPException(status_code=404, detail="Teacher not found")