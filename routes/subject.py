from fastapi import APIRouter, HTTPException, Depends, status
from models.subject_model import SubjectCreateModel, SubjectResponseModel
from typing import List
from database.mongo import AsyncDatabase
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from .auth import get_current_active_user

router = APIRouter()

def get_db():
    return AsyncDatabase.get_db()


@router.post("/", response_model=SubjectResponseModel, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectCreateModel, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    # This endpoint is also available to Admins through the /admin/subjects/ route
    subject_dict = subject.model_dump(by_alias=True)
    subject_dict["created_at"] = datetime.utcnow()
    subject_dict["is_active"] = True

    result = await db["subjects"].insert_one(subject_dict)
    
    if result.inserted_id:
        new_subject = await db["subjects"].find_one({"_id": result.inserted_id})
        return SubjectResponseModel(**new_subject)

    raise HTTPException(status_code=500, detail="Failed to create subject")


@router.get("/", response_model=List[SubjectResponseModel])
async def get_all_subjects(db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    subjects = []
    async for subject in db["subjects"].find():
        subjects.append(SubjectResponseModel(**subject))
    return subjects

@router.get("/{subject_id}", response_model=SubjectResponseModel)
async def get_subject(subject_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(subject_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    
    subject = await db["subjects"].find_one({"_id": ObjectId(subject_id)})
    
    if subject:
        return SubjectResponseModel(**subject)
    
    raise HTTPException(status_code=404, detail="Subject not found")
