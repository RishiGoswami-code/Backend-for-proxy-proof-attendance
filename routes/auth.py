from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.admin_model import AdminResponseModel
from models.student_model import StudentResponseModel
from models.teacher_model import TeacherResponseModel
from database.mongo import AsyncDatabase
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    return AsyncDatabase.get_db()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str, role: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    user = None
    collection_name = ""
    if role == "admin":
        collection_name = "admins"
    elif role == "teacher":
        collection_name = "teachers"
    elif role == "student":
        collection_name = "students"
    
    if collection_name:
        user = await db[collection_name].find_one({"email_id": email})
    
    if not user:
        return False
    
    if not verify_password(password, user.get("password")):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = None
    if role == "admin":
        user = await db["admins"].find_one({"email_id": email})
        if user:
            return AdminResponseModel(**user)
    elif role == "teacher":
        user = await db["teachers"].find_one({"email_id": email})
        if user:
            return TeacherResponseModel(**user)
    elif role == "student":
        user = await db["students"].find_one({"email_id": email})
        if user:
            return StudentResponseModel(**user)
    
    raise credentials_exception


async def get_current_active_user(current_user: Union[AdminResponseModel, StudentResponseModel, TeacherResponseModel] = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), role: str = "student", db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, role, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email_id'], "role": role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
