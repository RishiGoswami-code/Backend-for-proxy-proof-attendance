from fastapi import APIRouter, HTTPException
from models.attendance_model import AttendanceCreateModel, AttendanceResponseModel
from typing import List

router = APIRouter()

# Dummy database
fake_attendance_db = []

@router.post("/", response_model=AttendanceResponseModel)
async def mark_attendance(attendance: AttendanceCreateModel):
    attendance_dict = attendance.dict()
    attendance_dict["_id"] = "attendance_id_" + str(len(fake_attendance_db) + 1)
    attendance_dict["created_at"] = "2025-07-20T10:30:00"
    attendance_dict["status"] = "Present"
    fake_attendance_db.append(attendance_dict)
    return attendance_dict

@router.get("/", response_model=List[AttendanceResponseModel])
async def get_all_attendance():
    return fake_attendance_db

@router.get("/{attendance_id}", response_model=AttendanceResponseModel)
async def get_attendance(attendance_id: str):
    for attendance in fake_attendance_db:
        if attendance["_id"] == attendance_id:
            return attendance
    raise HTTPException(status_code=404, detail="Attendance record not found")

@router.get("/student/{student_id}", response_model=List[AttendanceResponseModel])
async def get_student_attendance(student_id: str):
    return [att for att in fake_attendance_db if att["student_id"] == student_id]

@router.get("/session/{session_id}", response_model=List[AttendanceResponseModel])
async def get_session_attendance(session_id: str):
    return [att for att in fake_attendance_db if att["session_id"] == session_id]