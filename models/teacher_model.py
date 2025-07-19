from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from bson import ObjectId
from typing import Optional, List


class teacherCreateModels(BaseModel):
  name: str = Field(..., examples='Achal Sir')
  subject: List = Field(..., examples=['Maths', "Data Handling In Python"])
  Batch: List = Field(..., examples=['Batch 2028 section A', 'Batch 2028 section B'])
  email_id: EmailStr = Field(..., examples="achal.sitare@sitare.org")
  
  