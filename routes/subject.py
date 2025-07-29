from fastapi import APIRouter, HTTPException
from models.subject_model import SubjectCreateModel, SubjectResponseModel
from typing import List

router = APIRouter()

# Dummy database
fake_subjects_db = []

@router.post("/", response_model=SubjectResponseModel)
async def create_subject(subject: SubjectCreateModel):
    subject_dict = subject.dict()
    subject_dict["_id"] = "subject_id_" + str(len(fake_subjects_db) + 1)
    subject_dict["created_at"] = "2025-07-19T15:29:45"
    subject_dict["is_active"] = True
    fake_subjects_db.append(subject_dict)
    return subject_dict

@router.get("/", response_model=List[SubjectResponseModel])
async def get_all_subjects():
    return fake_subjects_db

@router.get("/{subject_id}", response_model=SubjectResponseModel)
async def get_subject(subject_id: str):
    for subject in fake_subjects_db:
        if subject["_id"] == subject_id:
            return subject
    raise HTTPException(status_code=404, detail="Subject not found")