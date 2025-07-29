from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from .admin_model import PyObjectId


class SubjectCreateModel(BaseModel):
    subject_name: str = Field(..., example="Data structures and algorithm")
    batch: str = Field(..., example="BTech 2028")
    section: Optional[str] = Field(None, example="A")
    teacher_id: Optional[str] = Field(None)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'subject_name': 'Data structures and algorithm',
                'batch': "BTech 2028",
                'section': "B",
                'teacher_id': "teacher_id_here"
            }
        }


class SubjectResponseModel(SubjectCreateModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }
        allow_population_by_field_name = True
        schema_extra = {
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