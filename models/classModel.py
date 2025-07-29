from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from .admin_model import PyObjectId


class ClassCreateModel(BaseModel):
    batch_name: str = Field(..., example="Batch 2028")
    description: Optional[str] = Field(None, example="BTech 2028 Batch")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'batch_name': "Batch 2028",
                'description': "BTech 2028 Batch"
            }
        }


class ClassResponseModel(ClassCreateModel):
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
                'batch_name': "Batch 2028",
                'description': "BTech 2028 Batch",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True
            }
        }