from django.db import models
from django.contrib.auth.models import User


# Course model to store course details
class Course(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=100)  # Course name

    def __str__(self):
        return self.name

# StudentDetails model to store student information
class StudentDetails(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    full_name = models.CharField(max_length=255)  # Full name of the student
    father_name = models.CharField(max_length=255)  # Father's name
    mother_name = models.CharField(max_length=255)  # Mother's name
    age = models.PositiveIntegerField()  # Age of the student
    gender = models.CharField(max_length=10)  # Gender (e.g., Male, Female, etc.)
    address = models.TextField()  # Address of the student
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link to the Course model
    scholarship = models.CharField(max_length=200, null=True, blank=True)  # Scholarship amount (nullable)
    admission_date = models.DateField()  # Admission date
    admission_number = models.CharField(max_length=6, unique=True) # 6-digit unique admission number
    hosteler = models.BooleanField(default=False)  # True for hosteler, False for non-hosteler



    def __str__(self):
        return self.full_name

# Feedback model to store student feedback
class Feedback(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    student_name = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)  # Link to the StudentDetails model
    title = models.CharField(max_length=100)  # Title of the feedback
    content = models.TextField()  # Content of the feedback

    def __str__(self):
        return self.title

# LeaveRequest model to store leave requests from students
class LeaveRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DENIED = 'Denied'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied')
    ]

    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    student_name = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)  # Link to the StudentDetails model
    subject = models.CharField(max_length=100)  # Subject of the leave request
    from_date = models.DateField()  # Start date of the leave
    to_date = models.DateField()  # End date of the leave
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)  # Status of the leave request

    def __str__(self):
        return f"{self.student_name.full_name} - {self.subject}"
 


# HostelFeeDetails model to store hostel fee information and receipts
class HostelFeeDetails(models.Model):
    student = models.OneToOneField(StudentDetails, on_delete=models.CASCADE, related_name='hostel_fee_details')
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_receipt = models.FileField(upload_to='fee_receipts/', null=True, blank=True)
    receipt_uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - Fee Details"



class StudentFeeReceipt(models.Model):
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    receipt_file = models.FileField(upload_to='fee_receipts/')
   

    def __str__(self):
        return f"Receipt for {self.student.full_name}"
    
class Subject(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    subject_name = models.CharField(max_length=100)  # Name of the subject
    subject_code = models.CharField(max_length=20)  # Unique code for the subject
    semester = models.IntegerField()  # Semester number
    course_name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class Mark(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)  # Foreign key to Subject model
    student = models.ForeignKey('StudentDetails', on_delete=models.CASCADE, to_field='admission_number')  # Foreign key to StudentDetails using admission_number
    marks_obtained = models.FloatField()  # Marks obtained in the subject

    def __str__(self):
        return f"Mark for {self.subject} - {self.student.full_name}"

