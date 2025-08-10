from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from bson import ObjectId
from typing import Optional, List, Any
from .admin_model import PyObjectId


class TeacherCreateModel(BaseModel):
    name: str = Field(..., example='Achal Sir')
    subjects: List[str] = Field(..., example=['Maths', "Data Handling In Python"])
    batches: List[str] = Field(..., example=['BTech 2028 section A', 'BTech 2028 section B'])
    email_id: EmailStr = Field(..., example="achal.sitare@sitare.org")
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'name': "Achal Sir",
                'subjects': ['Maths', 'Data Handling In Python'],
                'batches': ['BTech 2028 section A', 'BTech 2028 section B'],
                'email_id': 'achal.sitare@sitare.org',
                'password': "teacherpassword123"
            }
        }
    )


class TeacherResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(..., example='Achal Sir')
    subjects: List[str] = Field(..., example=['Maths', "Data Handling In Python"])
    batches: List[str] = Field(..., example=['BTech 2028 section A', 'BTech 2028 section B'])
    email_id: EmailStr = Field(..., example="achal.sitare@sitare.org")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    device_token: Optional[str] = Field(None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        },
        json_schema_extra={
            'example': {
                '_id': "qwertyuiop",
                'name': "Achal Sir",
                'subjects': ['Maths', 'Data Handling In Python'],
                'batches': ['BTech 2028 section A', 'BTech 2028 section B'],
                'email_id': 'achal.sitare@sitare.org',
                'created_at': "2025-07-20T23:51:01",
                'is_active': True,
                'device_token': "fcm_token_here"
            }
        }
    )

