from fastapi import APIRouter, HTTPException, Depends, status
from models.classModel import ClassCreateModel, ClassResponseModel
from typing import List
from database.mongo import AsyncDatabase
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from .auth import get_current_active_user

router = APIRouter()

def get_db():
    return AsyncDatabase.get_db()

@router.post("/", response_model=ClassResponseModel, status_code=status.HTTP_201_CREATED)
async def create_class(class_: ClassCreateModel, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    # This endpoint is also available to Admins through the /admin/classes/ route
    class_dict = class_.model_dump(by_alias=True)
    class_dict["created_at"] = datetime.utcnow()
    class_dict["is_active"] = True

    result = await db["classes"].insert_one(class_dict)
    
    if result.inserted_id:
        new_class = await db["classes"].find_one({"_id": result.inserted_id})
        return ClassResponseModel(**new_class)

    raise HTTPException(status_code=500, detail="Failed to create class")


@router.get("/", response_model=List[ClassResponseModel])
async def get_all_classes(db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    classes = []
    async for class_ in db["classes"].find():
        classes.append(ClassResponseModel(**class_))
    return classes

@router.get("/{class_id}", response_model=ClassResponseModel)
async def get_class(class_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(class_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    
    class_ = await db["classes"].find_one({"_id": ObjectId(class_id)})

    if class_:
        return ClassResponseModel(**class_)
    
    raise HTTPException(status_code=404, detail="Class not found")
