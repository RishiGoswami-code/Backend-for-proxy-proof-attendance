from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from .admin_model import PyObjectId


class SubjectCreateModel(BaseModel):
    subject_name: str = Field(..., example="Data structures and algorithm")
    batch: str = Field(..., example="BTech 2028")
    section: Optional[str] = Field(None, example="A")
    teacher_id: Optional[str] = Field(None)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'subject_name': 'Data structures and algorithm',
                'batch': "BTech 2028",
                'section': "B",
                'teacher_id': "teacher_id_here"
            }
        }
    )


class SubjectResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    subject_name: str = Field(..., example="Data structures and algorithm")
    batch: str = Field(..., example="BTech 2028")
    section: Optional[str] = Field(None, example="A")
    teacher_id: Optional[str] = Field(None)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        },
        json_schema_extra={
            'example': {
                '_id': 'esurf1234vj324n',
                'subject_name': "Data structures and algorithm",
                'batch': "BTech 2028",
                'section': "B",
                'teacher_id': "teacher_id_here",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True
            }
        }
    )

