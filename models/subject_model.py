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



class subjectCreateModel(BaseModel):
  subject_name : str = Field(..., examples="Data structures and algorithm")
  batch: str = Field(..., examples="Btech 2028")
  section: Optional[str] = Field(examples="A")

  class config:
    allow_population_by_class = True
    schema_extra = {
      'example': {
        'subject_name': 'Chandan Giri',
        'batch': "Batch 2028",
        'section': "B"
      }
    }

class subjectResponsemodel(subjectCreateModel):
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
        'subject_name': "Data structures and algorithm",
        'batch': "Batch 2028",
        'section': "B",
        'created_at': "19/07/2025T15:29:45"
      }
    }

    



