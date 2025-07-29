from .admin import router as admin_router
from .student import router as student_router
from .teacher import router as teacher_router
from .classRoutes import router as class_router
from .subject import router as subject_router
from .attendance import router as attendance_router

__all__ = [
    'admin_router',
    'student_router',
    'teacher_router',
    'class_router',
    'subject_router',
    'attendance_router'
]