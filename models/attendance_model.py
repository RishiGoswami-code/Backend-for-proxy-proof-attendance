from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId


class pyobjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate  # No need to call it here, just pass the function

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Not a valid object ID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
