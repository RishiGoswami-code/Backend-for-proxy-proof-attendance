from fastapi import APIRouter, Depends, HTTPException, status
from models.admin_model import AdminModel, AdminResponseModel
from models.teacher_model import TeacherCreateModel, TeacherResponseModel
from models.student_model import StudentCreateModel, StudentResponseModel
from models.classModel import ClassCreateModel, ClassResponseModel
from models.subject_model import SubjectCreateModel, SubjectResponseModel
from database.mongo import AsyncDatabase
from typing import List
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from .auth import get_current_active_user, get_password_hash

router = APIRouter()

def get_db():
    return AsyncDatabase.get_db()

@router.post("/", response_model=AdminResponseModel, status_code=status.HTTP_201_CREATED)
async def create_admin(admin: AdminModel, db: AsyncIOMotorDatabase = Depends(get_db)):
    admin_dict = admin.model_dump(by_alias=True)
    admin_dict["created_at"] = datetime.utcnow()
    admin_dict["is_active"] = True
    admin_dict["password"] = get_password_hash(admin_dict["password"])
    
    result = await db["admins"].insert_one(admin_dict)
    
    if result.inserted_id:
        new_admin = await db["admins"].find_one({"_id": result.inserted_id})
        return AdminResponseModel(**new_admin)

    raise HTTPException(status_code=500, detail="Failed to create admin")


@router.get("/", response_model=List[AdminResponseModel])
async def get_all_admins(db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    admins = []
    async for admin in db["admins"].find():
        admins.append(AdminResponseModel(**admin))
    return admins

@router.get("/{admin_id}", response_model=AdminResponseModel)
async def get_admin(admin_id: str, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    if not ObjectId.is_valid(admin_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    
    admin = await db["admins"].find_one({"_id": ObjectId(admin_id)})
    
    if admin:
        return AdminResponseModel(**admin)
    
    raise HTTPException(status_code=404, detail="Admin not found")


# --- Teacher Management (Admin's role) ---
@router.post("/teachers/", response_model=TeacherResponseModel, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: TeacherCreateModel, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    teacher_dict = teacher.model_dump(by_alias=True)
    teacher_dict["created_at"] = datetime.utcnow()
    teacher_dict["is_active"] = True
    teacher_dict["password"] = get_password_hash(teacher_dict["password"])
    
    result = await db["teachers"].insert_one(teacher_dict)
    if result.inserted_id:
        new_teacher = await db["teachers"].find_one({"_id": result.inserted_id})
        return TeacherResponseModel(**new_teacher)
    raise HTTPException(status_code=500, detail="Failed to create teacher")


# --- Student Management (Admin's role) ---
@router.post("/students/", response_model=StudentResponseModel, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreateModel, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    student_dict = student.model_dump(by_alias=True)
    student_dict["created_at"] = datetime.utcnow()
    student_dict["is_active"] = True
    student_dict["password"] = get_password_hash(student_dict["password"])
    
    result = await db["students"].insert_one(student_dict)
    if result.inserted_id:
        new_student = await db["students"].find_one({"_id": result.inserted_id})
        return StudentResponseModel(**new_student)
    raise HTTPException(status_code=500, detail="Failed to create student")


# --- Class Management (Admin's role) ---
@router.post("/classes/", response_model=ClassResponseModel, status_code=status.HTTP_201_CREATED)
async def create_class(class_: ClassCreateModel, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    class_dict = class_.model_dump(by_alias=True)
    class_dict["created_at"] = datetime.utcnow()
    class_dict["is_active"] = True
    
    result = await db["classes"].insert_one(class_dict)
    if result.inserted_id:
        new_class = await db["classes"].find_one({"_id": result.inserted_id})
        return ClassResponseModel(**new_class)
    raise HTTPException(status_code=500, detail="Failed to create class")


# --- Subject Management (Admin's role) ---
@router.post("/subjects/", response_model=SubjectResponseModel, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectCreateModel, db: AsyncIOMotorDatabase = Depends(get_db), current_user = Depends(get_current_active_user)):
    subject_dict = subject.model_dump(by_alias=True)
    subject_dict["created_at"] = datetime.utcnow()
    subject_dict["is_active"] = True
    
    result = await db["subjects"].insert_one(subject_dict)
    if result.inserted_id:
        new_subject = await db["subjects"].find_one({"_id": result.inserted_id})
        return SubjectResponseModel(**new_subject)
    raise HTTPException(status_code=500, detail="Failed to create subject")
