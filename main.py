from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Use absolute imports for routes from the top-level package
from routes import admin, student, teacher, classRoutes, subject, attendance
from database.mongo import AsyncDatabase

# Load environment variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the application startup and shutdown events.
    Connects to the database on startup and closes the connection on shutdown.
    """
    await AsyncDatabase.connect()
    yield
    await AsyncDatabase.close()


app = FastAPI(
    title="Proxy proof attendance system",
    description="Backend for attendance using QR + Bluetooth + Face Recognition",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(student.router, prefix="/student", tags=["Student"])
app.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
app.include_router(classRoutes.router, prefix="/class", tags=["Class"])
app.include_router(subject.router, prefix="/subject", tags=["Subject"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Proxy-Proof Attendance System"}
