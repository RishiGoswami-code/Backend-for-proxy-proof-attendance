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



class studentCreateModel(BaseModel):
  name : str = Field(..., examples="Chandan Giri")
  batch: str = Field(..., examples="Btech 2028")
  roll_num: str = Field(..., examples='202410101XXX')
  email_id: EmailStr = Field(..., examples="su-24036@sitare.org")
  section: Optional[str] = Field(examples="A")

  class config:
    allow_population_by_class = True
    schema_extra = {
      'example': {
        'name': 'Chandan Giri',
        'batch': "Batch 2028",
        'roll_num': '202410101XXX', 
        'email_id': "su-24036@sitare.org", 
        'section': "B"
      }
    }

class StudentResponsemodel(studentCreateModel):
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
        'name': "Chandan Giri",
        'batch': "Batch 2028",
        "email_id": "su-2024@sitare.org",
        'roll_num': '202410101XXX',
        'section': "B",
        'created_at': "19/07/2025T15:29:45"
      }
    }

    



