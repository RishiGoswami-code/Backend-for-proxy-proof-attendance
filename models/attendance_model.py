from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from .admin_model import PyObjectId


class AttendanceCreateModel(BaseModel):
    student_id: str = Field(..., description="ID of the student")
    subject_id: str = Field(..., description="ID of the subject")
    class_id: str = Field(..., description="ID of the class")
    teacher_id: str = Field(..., description="ID of the teacher")
    session_id: str = Field(..., description="ID of the attendance session")
    location: dict = Field(..., description="GPS coordinates of attendance")
    image_url: str = Field(..., description="URL of the captured image")
    is_proxy: bool = Field(False, description="Flag for proxy detection")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'student_id': "student_id_here",
                'subject_id': "subject_id_here",
                'class_id': "class_id_here",
                'teacher_id': "teacher_id_here",
                'session_id': "session_id_here",
                'location': {"lat": 26.9124, "lng": 75.7873},
                'image_url': "https://storage.example.com/image.jpg",
                'is_proxy': False
            }
        }
    )


class AttendanceResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    student_id: str = Field(..., description="ID of the student")
    subject_id: str = Field(..., description="ID of the subject")
    class_id: str = Field(..., description="ID of the class")
    teacher_id: str = Field(..., description="ID of the teacher")
    session_id: str = Field(..., description="ID of the attendance session")
    location: dict = Field(..., description="GPS coordinates of attendance")
    image_url: str = Field(..., description="URL of the captured image")
    is_proxy: bool = Field(False, description="Flag for proxy detection")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field("Present", description="Attendance status")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        },
        json_schema_extra={
            'example': {
                '_id': "attendance_id_here",
                'student_id': "student_id_here",
                'subject_id': "subject_id_here",
                'class_id': "class_id_here",
                'teacher_id': "teacher_id_here",
                'session_id': "session_id_here",
                'location': {"lat": 26.9124, "lng": 75.7873},
                'image_url': "https://storage.example.com/image.jpg",
                'is_proxy': False,
                'created_at': "2025-07-20T10:30:00",
                'status': "Present"
            }
        }
    )

