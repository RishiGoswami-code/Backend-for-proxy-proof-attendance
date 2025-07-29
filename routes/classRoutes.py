from fastapi import APIRouter, HTTPException
from models.classModel import ClassCreateModel, ClassResponseModel
from typing import List

router = APIRouter()

# Dummy database
fake_classes_db = []

@router.post("/", response_model=ClassResponseModel)
async def create_class(class_: ClassCreateModel):
    class_dict = class_.dict()
    class_dict["_id"] = "class_id_" + str(len(fake_classes_db) + 1)
    class_dict["created_at"] = "2025-07-19T15:29:45"
    class_dict["is_active"] = True
    fake_classes_db.append(class_dict)
    return class_dict

@router.get("/", response_model=List[ClassResponseModel])
async def get_all_classes():
    return fake_classes_db

@router.get("/{class_id}", response_model=ClassResponseModel)
async def get_class(class_id: str):
    for class_ in fake_classes_db:
        if class_["_id"] == class_id:
            return class_
    raise HTTPException(status_code=404, detail="Class not found")