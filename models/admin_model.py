from pydantic import BaseModel, EmailStr, Field, ConfigDict, GetCoreSchemaHandler
from typing import Optional, Any, Dict
from datetime import datetime
from bson import ObjectId
from pydantic_core import CoreSchema


# Pydantic v2 replaces the nested Config class with a ConfigDict
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetCoreSchemaHandler
    ) -> Dict[str, Any]:
        json_schema = handler(core_schema)
        json_schema['type'] = 'string'
        return json_schema


class AdminModel(BaseModel):
    name: str = Field(..., example="Amit Singhal")
    email_id: EmailStr = Field(..., example="amit@sitare.org")
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            'example': {
                'name': 'Amit Singhal',
                'email_id': "amit@sitare.org",
                'password': "securepassword123"
            }
        }
    )


class AdminResponseModel(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(..., example="Amit Singhal")
    email_id: EmailStr = Field(..., example="amit@sitare.org")
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
                'name': "Amit Singhal",
                "email_id": "amit@sitare.org",
                'created_at': "2025-07-19T15:29:45",
                'is_active': True
            }
        }
    )

