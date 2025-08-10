from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from .admin_model import PyObjectId


class ClassCreateModel(BaseModel):
    batch_name: str = Field(..., example="Batch 2028")
    description: Optional[str] = Field(None, example="BTech 2028 Batch")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'batch_name': "Batch 2028",
                'description': "BTech 2028 Batch"
            }
        }
    )


class ClassResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    batch_name: str = Field(..., example="Batch 2028")
    description: Optional[str] = Field(None, example="BTech 2028 Batch")
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
                'batch_name': "Batch 2028",
                'description': "BTech 2028 Batch",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True
            }
        }
    )

