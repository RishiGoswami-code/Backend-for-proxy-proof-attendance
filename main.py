from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import admin, student, teacher, classRoutes, subject, attendance

app = FastAPI(
    title="Proxy proof attendance system",
    description="Backend for attendance using QR + Bluetooth + Face Recognition",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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