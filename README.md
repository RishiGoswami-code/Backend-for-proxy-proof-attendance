# 📦 Smart Attendance System – Backend (FastAPI)

Welcome to the **backend repository** of the **Smart Proxy-Proof Attendance System** – a next-gen solution designed to **eliminate proxy attendance** using dynamic QR codes, Bluetooth proximity detection, and AI-based face recognition with liveness checks.

---

## 🧠 Features

- 🔐 Secure **Login & Signup** for students, teachers, and admins  
- 🧾 **JWT-based Authentication** and role-based access  
- 📸 **Face Recognition & Liveness Detection** integration  
- 📡 **Bluetooth Proximity Detection** to validate student presence  
- 🌀 **Rotating QR Code** system for class attendance  
- 🧠 **Proxy Prevention** with face & device verification  
- 📊 **Admin Dashboards** with attendance insights & reports  
- ⚠️ Fake face detection & user warning system  
- 📁 Profile management and subject/session assignment  
- 🔍 Real-time stats for today, per session, or full records  

---

## ⚙️ Tech Stack

| Layer         | Stack                   |
|---------------|-------------------------|
| Backend       | FastAPI (Python)        |
| Database      | MongoDB (Motor ORM)     |
| Auth          | JWT Tokens              |
| Face Detection| OpenCV / DeepFace       |
| QR Generator  | qrcode / custom logic   |
| Bluetooth     | Handled via mobile app  |
| Deployment    | Vercel / Heroku / Firebase (Optional) |

---

## 📁 Project Structure



---

## 🚀 How It Works (Backend Flow)

1. **Teacher creates session** → generates QR  
2. **Student scans QR** → verifies:
   - Proximity to teacher via Bluetooth  
   - Face matches their profile (liveness verified)  
3. If all pass → attendance marked ✅  
4. If mismatch or fake attempt → warning logged ❌  

---

## 🔐 Authentication Flow

- Passwords are securely hashed  
- JWT is generated on login  
- Each API validates the user’s role (admin, teacher, student)

---

## 🧪 Routes Overview

- `POST /register/student` – Signup as student  
- `POST /register/teacher` – Signup as teacher  
- `POST /register/admin` – Admin registration  
- `POST /login` – Role-based login  
- `GET /profile/{id}` – View user profile  
- `PUT /profile/update/{id}` – Update user profile  
- `GET /qr/generate/{session_id}` – Generate rotating QR  
- `POST /qr/scan` – Scan QR for session  
- `POST /face/verify` – Verify face image  
- `POST /bluetooth/check` – Bluetooth proximity validation  
- `POST /attendance/mark` – Mark attendance if all checks pass  
- `GET /attendance/statistics/today/{user_id}` – Today’s stats  
- `GET /attendance/statistics/all/{user_id}` – All-time stats  
- `GET /attendance/data/class/{class_id}` – Per class  
- `GET /attendance/data/subject/{subject_id}` – Per subject  
- `GET /admin/student-profile/{student_id}` – Admin view  
- `GET /admin/stats` – Dashboard metrics  
- `GET /warned-users` – List of warned students  
- `GET /errors` – Error logs  


---

## 🧭 Setup Instructions

### 🔧 Clone & Setup

```bash
git clone https://github.com/your-username/smart-attendance-backend.git
cd smart_attendance_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
