# Student Management System

A comprehensive web-based Student Management System built with Django. This system is designed around a secure, role-based architecture to streamline communication and data management between administrators, teachers, and students.

## 🏗️ Architecture Overview

The system is built on a shared data layer containing **Users & Accounts**, **Courses & Subjects**, and **Files & Records**. Access to this data is securely routed through a central **Login & Authentication** module which detects the user's role (Username + Password based).

Below are the feature modules available to each role:

---

### 🟣 Admin (Principal / Management)
**Admin Dashboard:** High-level overview featuring system stats, student distribution charts, and leave alerts.

**Feature Modules:**
- 👤 **User Management:** Securely create and manage accounts for both students and teachers.
- 📚 **Course & Subject Mgmt:** Create classes (courses) and assign specific subjects to them.
- 🏢 **Hostel Fee Tracking:** Log hostel fee payments and generate receipts for students.
- 💬 **Feedback Review:** Read and manage feedback submissions from students.
- ✅ **Leave Approval:** Review, approve, or reject leave requests submitted by students.

---

### 🟢 Teacher (Staff / Instructor)
**Teacher Dashboard:** Dedicated hub showing total students, active courses, and quick-action shortcuts.

**Feature Modules:**
- 📅 **Attendance Marking:** Track daily attendance by marking students as Present, Absent, or Late.
- 📤 **Material Upload:** Upload PDFs, assignments, and study materials categorized by course.
- 📝 **Marks Entry:** Input test scores and grades for students per subject.
- *(Note: Teachers can also review and manage student leave requests directly from their dashboard).*

---

### 🟠 Student (Enrolled Learner)
**Student Dashboard:** Personalized view featuring their overall attendance percentage and a line chart of their marks over time.

**Feature Modules:**
- 🆔 **My Profile:** Fill out and update their personal details (strictly isolated to their own account).
- 📊 **My Attendance:** View their personal historical records of present/absent days.
- 📖 **Study Materials:** View and securely download files/notes uploaded by their teachers.
- 🗓️ **Leave Request:** Submit absence reasons which are forwarded to Teachers/Admins for approval.

---

## 🛠️ Tech Stack
- **Backend:** Python, Django Framework
- **Frontend:** HTML5, CSS3, Bootstrap 4, Font-Awesome (Icons)
- **Database:** SQLite (Shared Data Layer for Roles/Courses/Records)
- **Data Visualization:** Chart.js

## 🚀 Project Setup & Installation

**1. Clone the Repository**
```bash
git clone <your-repository-url>
cd Studentmanagementsystem-main
```

**2. Create a Virtual Environment**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

**3. Install Dependencies & Migrate**
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

**4. Create Admin Account & Run Server**
```bash
python manage.py createsuperuser
python manage.py runserver 8080
```
Visit `http://127.0.0.1:8080/` in your web browser. 

*(Note: Students cannot sign themselves up. Admins/Teachers must create user accounts for them to ensure secure access).*
