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



class classCreateModel(BaseModel):
  batch_name : str = Field(..., examples="Batch 2028")
  

  class config:
    allow_population_by_class = True
    schema_extra = {
      'example': {
        'batch_name': "Batch 2028",
      }
    }

class classResponsemodel(classCreateModel):
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
        'batch': "Batch 2028",
        'created_at': "19/07/2025T15:29:45"
      }
    }

    



