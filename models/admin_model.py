from pydantic import BaseModel, json, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime


class pyobjectID(ObjectId):
  @classmethod
  def __get_validators__(cls):
    yield cls.validate
  @classmethod
  def validate(cls, v):
    if not object.is_valid(v):
      raise ValueError("Invalid ObjectID")
    return ObjectId(v)
  
  @classmethod
  def __modify_schema__(cls, feild_schema):
    feild_schema.update(type="string")



class adminModel(BaseModel):
  name : str = Field(..., examples="Amit Singhal")
  email_id: EmailStr = Field(..., examples="amit@sitare.org")

  class config:
    allow_population_by_class = True
    schema_extra = {
      'example': {
        'name': 'Amit Singhal',
        'email_id': "amit@sitare.org", 
      }
    }

class adminResponsemodel(adminModel):
  id: pyobjectID= Field(default_factory = pyobjectID, alias='_id')
  created_at: Optional[datetime] = Field(default_factory=datetime.utcnow )

  class config:
    json_encoder ={
      ObjectId: str,
      datetime: lambda v: v.isoformat(),}
    allow_population_by_field_name = True
    schema_extra = {
      'example':{
        '_id': 'esurf1234vj324n',
        'name': "Amit Singhal",
        "email_id": "amit@sitare.org",
        'created_at': "19/07/2025T15:29:45"
      }
    }

    



