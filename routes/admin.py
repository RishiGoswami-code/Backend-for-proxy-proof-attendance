from fastapi import APIRouter, Depends, HTTPException, status
from models.admin_model import AdminModel, AdminResponseModel
from typing import List

router = APIRouter()

# Dummy database
fake_admins_db = []

@router.post("/", response_model=AdminResponseModel)
async def create_admin(admin: AdminModel):
    admin_dict = admin.dict()
    admin_dict["_id"] = "admin_id_" + str(len(fake_admins_db) + 1)
    admin_dict["created_at"] = "2025-07-19T15:29:45"
    admin_dict["is_active"] = True
    fake_admins_db.append(admin_dict)
    return admin_dict

@router.get("/", response_model=List[AdminResponseModel])
async def get_all_admins():
    return fake_admins_db

@router.get("/{admin_id}", response_model=AdminResponseModel)
async def get_admin(admin_id: str):
    for admin in fake_admins_db:
        if admin["_id"] == admin_id:
            return admin
    raise HTTPException(status_code=404, detail="Admin not found")