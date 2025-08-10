from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from .admin_model import PyObjectId


class StudentCreateModel(BaseModel):
    name: str = Field(..., example="Chandan Giri")
    batch: str = Field(..., example="BTech 2028")
    roll_num: str = Field(..., example='202410101XXX')
    email_id: EmailStr = Field(..., example="su-24036@sitare.org")
    section: Optional[str] = Field(None, example="A")
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'name': 'Chandan Giri',
                'batch': "BTech 2028",
                'roll_num': '202410101XXX',
                'email_id': "su-24036@sitare.org",
                'section': "B",
                'password': "studentpassword123"
            }
        }
    )


class StudentResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(..., example="Chandan Giri")
    batch: str = Field(..., example="BTech 2028")
    roll_num: str = Field(..., example='202410101XXX')
    email_id: EmailStr = Field(..., example="su-24036@sitare.org")
    section: Optional[str] = Field(None, example="A")
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
                '_id': 'esurf1234vj324n',
                'name': "Chandan Giri",
                'batch': "BTech 2028",
                'roll_num': '202410101XXX',
                'email_id': "su-24036@sitare.org",
                'section': "B",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True,
                'device_token': "fcm_token_here"
            }
        }
    )

