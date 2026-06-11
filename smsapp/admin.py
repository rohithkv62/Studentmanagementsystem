from django.contrib import admin
from .models import (StudentDetails, Course, Feedback, LeaveRequest,HostelFeeDetails)


# Register the Course model with the admin site
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name in the admin list view

# Register the StudentDetails model with the admin site
@admin.register(StudentDetails)
class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'course_name', 'admission_number', 'hosteler')  # Display selected fields in the admin list view
    search_fields = ('full_name', 'admission_number')  # Enable search by full name and admission number

# Register the Feedback model with the admin site
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'title')  # Display student name and title in the admin list view
    search_fields = ('title',)  # Enable search by title

# Register the LeaveRequest model with the admin site
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'subject', 'status', 'from_date', 'to_date')  # Display selected fields in the admin list view
    list_filter = ('status',)  # Enable filtering by status
    search_fields = ('subject',)  # Enable search by subject

# Register the HostelFeeDetails model with the admin site
@admin.register(HostelFeeDetails)
class HostelFeeDetailsAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_amount', 'fee_receipt', 'receipt_uploaded_at')  # Display selected fields in the admin list view
    search_fields = ('student__full_name',)  # Enable search by student name
    list_filter = ('receipt_uploaded_at',)  # Enable filtering by receipt upload date
    