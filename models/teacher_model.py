from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from bson import ObjectId
from typing import Optional, List
from student_model import pyobjectID



class teacherCreateModels(BaseModel):
  name: str = Field(..., examples='Achal Sir')
  subject: List = Field(..., examples=['Maths', "Data Handling In Python"])
  Batch: List = Field(..., examples=['Batch 2028 section A', 'Batch 2028 section B'])
  email_id: EmailStr = Field(..., examples="achal.sitare@sitare.org")
  
  class config:
    allow_data_from_field = True
    schema_extra = {
      'examples': {
        '_id':"qwertyuiop",
        'name':"Achal Sir", 
        'subject':['Maths', 'Data Handling In Python'],
        'Batch':['Batch 2028 section A', 'Batch 2028 section B'],
        'email_id':'achal.sitare@sitare.org',
        'create_at':"20/07/2025T23:51:1",
      }
    }

class teacherResponseModels(teacherCreateModels):
  id: pyobjectID= Field(default_factory = pyobjectID, alias='_id')
  created_at: Optional[datetime] = Field(default_factory=datetime.utcnow )

  class config:
    allow_data_from_field = True
    json_encoder ={
      ObjectId: str,
      datetime: lambda v: v.isoformat(),}
    schema_extra = {
      'examples': {
        '_id':"qwertyuiop",
        'name':"Achal Sir", 
        'subject':['Maths', 'Data Handling In Python'],
        'Batch':['Batch 2028 section A', 'Batch 2028 section B'],
        'email_id':'achal.sitare@sitare.org',
        'create_at':"20/07/2025T23:51:1",
      }
    }

  