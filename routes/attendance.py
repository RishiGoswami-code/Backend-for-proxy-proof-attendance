import qrcode
import base64
import face_recognition
import cv2
import numpy as np
from io import BytesIO
from fastapi import APIRouter, HTTPException, Depends, status, Body
from fastapi.responses import JSONResponse
from models.attendance_model import AttendanceCreateModel, AttendanceResponseModel
from typing import List, Optional
from database.mongo import AsyncDatabase
from bson import ObjectId
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from .auth import get_current_active_user
from models.student_model import StudentResponseModel
from models.teacher_model import TeacherResponseModel
from pydantic import BaseModel

router = APIRouter()

# In-memory storage for active attendance sessions
# In a production environment, this would be stored in a a persistent cache like Redis.
active_sessions = {}

def get_db():
    return AsyncDatabase.get_db()

def is_within_proximity(teacher_bt_id: str, student_bt_id: str) -> bool:
    """
    Simulates a Bluetooth proximity check.
    In a real app, this would involve a server-side service checking
    if the two Bluetooth device IDs are within range of each other.
    For this mock implementation, we always return True.
    """
    print(f"Simulating proximity check for teacher: {teacher_bt_id} and student: {student_bt_id}")
    return True

def compare_faces(known_face_image_path: str, live_image_data: str) -> bool:
    """
    Compares a live image to a known face image using face recognition.
    
    Args:
        known_face_image_path: Path to the pre-registered image of the student.
        live_image_data: Base64-encoded string of the live captured image.

    Returns:
        True if the faces match, False otherwise.
    """
    # This is a placeholder. You would need to store student face data as embeddings
    # and compare the live image embedding to the stored one.
    
    # Decode the base64 string to an image
    image_bytes = base64.b64decode(live_image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    live_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert live image to RGB
    live_image_rgb = cv2.cvtColor(live_image, cv2.COLOR_BGR2RGB)
    
    try:
        # Find all the faces in the live image
        face_locations = face_recognition.face_locations(live_image_rgb)
        if not face_locations:
            print("No face detected in the live image.")
            return False

        # Get the face encoding for the live image
        live_face_encoding = face_recognition.face_encodings(live_image_rgb, face_locations)[0]

        # In a real system, you would have a stored encoding in the database
        # and load it here. For this example, we'll use a mock stored image.
        # This part requires a valid image path to work.
        known_image = face_recognition.load_image_file(known_face_image_path)
        known_face_encoding = face_recognition.face_encodings(known_image)[0]

        # Compare the faces and get the distance
        matches = face_recognition.compare_faces([known_face_encoding], live_face_encoding)
        face_distance = face_recognition.face_distance([known_face_encoding], live_face_encoding)
        
        print(f"Face match result: {matches[0]}, Face distance: {face_distance[0]}")
        
        # A lower distance means a better match. The threshold is typically around 0.6.
        # We check both the match result and the distance for robustness.
        if matches[0] and face_distance[0] < 0.6:
            return True
        else:
            return False

    except IndexError:
        # No faces found in the images
        print("No face found in one of the images.")
        return False
    except Exception as e:
        print(f"Error during face recognition: {e}")
        return False

# Pydantic model for starting an attendance session
class AttendanceSessionStartModel(BaseModel):
    subject_name: str
    class_name: str

@router.post("/start-session", status_code=status.HTTP_201_CREATED)
async def start_attendance_session(
    session_data: AttendanceSessionStartModel, 
    db: AsyncIOMotorDatabase = Depends(get_db), 
    current_user: TeacherResponseModel = Depends(get_current_active_user)
):
    """
    Endpoint for a teacher to start a new attendance session.
    Generates a unique, time-based QR code token.
    """
    teacher_id = str(current_user.id)
    
    # Check if the teacher is assigned to the class and subject
    # We now query by subject_name and teacher_id to be more robust
    subject = await db["subjects"].find_one({"subject_name": session_data.subject_name, "teacher_id": teacher_id})
    if not subject:
        raise HTTPException(status_code=403, detail="You are not authorized to start a session for this subject.")

    # Create a unique session token
    session_id = str(ObjectId())
    
    # The token payload includes session metadata for student validation
    payload = {
        "session_id": session_id,
        "teacher_id": teacher_id,
        "class_id": session_data.class_name,
        "subject_id": str(subject["_id"]), # Store the actual ObjectId for the subject
        "exp": (datetime.utcnow() + timedelta(minutes=2)).timestamp() # Token expires in 2 minutes
    }
    
    # Store the active session in memory
    active_sessions[session_id] = payload

    # Create the QR code data with the token
    qr_data = f"attendance_token:{session_id}"
    qr_img = qrcode.make(qr_data)
    
    # Convert the QR code image to a base64 string for easy transfer
    qr_img_bytes = BytesIO()
    qr_img.save(qr_img_bytes, format="PNG")
    qr_b64 = base64.b64encode(qr_img_bytes.getvalue()).decode()

    return {
        "session_id": session_id,
        "qr_code_image": f"data:image/png;base64,{qr_b64}",
        "message": "Attendance session started. Please display the QR code for students to scan."
    }

class AttendanceMarkRequest(BaseModel):
    session_id: str
    student_id: str
    student_bt_id: str # Student's Bluetooth ID
    live_image_base64: str

@router.post("/mark", response_model=AttendanceResponseModel)
async def mark_attendance(
    request: AttendanceMarkRequest, 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Endpoint for a student to mark attendance. This is the core proxy detection logic.
    It performs a multi-layered verification:
    1. Session/QR code validation.
    2. Simulated Bluetooth proximity check.
    3. Biometric facial recognition.
    """
    # Step 1: Validate the session token from the QR code
    session_payload = active_sessions.get(request.session_id)
    if not session_payload or datetime.utcnow().timestamp() > session_payload["exp"]:
        raise HTTPException(status_code=400, detail="Invalid or expired attendance session.")

    # Step 2: Simulate Bluetooth proximity check
    # In a real app, the teacher's BT ID would be stored in the session payload
    teacher_bt_id = "mock_teacher_bt_id" # This would come from the teacher's session data
    if not is_within_proximity(teacher_bt_id, request.student_bt_id):
        raise HTTPException(status_code=400, detail="Proxy attendance detected: Not within proximity of the teacher's device.")

    # Step 3: Biometric facial recognition check
    student = await db["students"].find_one({"_id": ObjectId(request.student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    # Get the student's reference face image path.
    # In a real system, you would have a stored image or embedding path.
    # Here, we use a placeholder path for demonstration.
    known_face_image_path = "path/to/student_face.jpg"
    
    is_proxy_detected = not compare_faces(known_face_image_path, request.live_image_base64)
    
    # Create the attendance record
    attendance_record = {
        "student_id": request.student_id,
        "subject_id": session_payload["subject_id"],
        "class_id": session_payload["class_id"],
        "teacher_id": session_payload["teacher_id"],
        "session_id": request.session_id,
        "location": {"lat": 0, "lng": 0}, # Placeholder, real app would capture this
        "image_url": "mock_image_url", # Placeholder for the uploaded image URL
        "is_proxy": is_proxy_detected,
        "created_at": datetime.utcnow(),
        "status": "Present" if not is_proxy_detected else "Proxy Detected"
    }
    
    result = await db["attendance"].insert_one(attendance_record)
    if result.inserted_id:
        new_record = await db["attendance"].find_one({"_id": result.inserted_id})
        return AttendanceResponseModel(**new_record)

    raise HTTPException(status_code=500, detail="Failed to mark attendance.")

@router.get("/my-attendance", response_model=List[AttendanceResponseModel])
async def get_my_attendance(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: StudentResponseModel = Depends(get_current_active_user)
):
    """Student endpoint to view their own attendance records."""
    attendance_records = []
    async for record in db["attendance"].find({"student_id": str(current_user.id)}):
        attendance_records.append(AttendanceResponseModel(**record))
    return attendance_records
