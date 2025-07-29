from pydantic import BaseModel, EmailStr, Field
from typing import Optional
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

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'name': 'Chandan Giri',
                'batch': "BTech 2028",
                'roll_num': '202410101XXX',
                'email_id': "su-24036@sitare.org",
                'section': "B",
                'password': "studentpassword123"
            }
        }


class StudentResponseModel(StudentCreateModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    device_token: Optional[str] = Field(None)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                '_id': 'esurf1234vj324n',
                'name': "Chandan Giri",
                'batch': "BTech 2028",
                "email_id": "su-24036@sitare.org",
                'roll_num': '202410101XXX',
                'section': "B",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True,
                'device_token': "fcm_token_here"
            }
        }