from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class AdminModel(BaseModel):
    name: str = Field(..., example="Amit Singhal")
    email_id: EmailStr = Field(..., example="amit@sitare.org")
    password: str = Field(..., min_length=6)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'name': 'Amit Singhal',
                'email_id': "amit@sitare.org",
                'password': "securepassword123"
            }
        }


class AdminResponseModel(AdminModel):
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
                'name': "Amit Singhal",
                "email_id": "amit@sitare.org",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True
            }
        }