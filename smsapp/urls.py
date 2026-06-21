from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *  # This imports all views from views.py

from .views import edit_student
from .views import mark_notifications_read

urlpatterns = [
    path('add_user/', add_user, name='add_user'),
    path('add_course/', add_course, name='add_course'),
    path('', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('landing/', landing_page, name='landing_page'),
    path('students/', students_page, name='students_page'),
    path('teachers/', teachers_page, name='teachers_page'),
    path('fees/', fee_management_page, name='fee_management_page'),
    path('hostels/', hostel_management_page, name='hostel_management_page'),
    path('logout/', user_logout, name='logout'),
    path('add_student/', add_student, name='add_student'),
    path('add_feedback/', add_feedback, name='add_feedback'),
    path('add_leave_request/', add_leave_request, name='add_leave_request'),
    path('courses/', courses, name='courses'),
    path('courses/<int:course_id>/students/', course_students, name='course_students'),
    path('feedback/', feedback_list, name='feedback_list'),
    path('view_leave_requests/', view_leave_requests, name='view_leave_requests'),
    path('leave-status/', student_leave_status, name='student_leave_status'),
    path('hostel_fee_details/', hostel_fee_details, name='hostel_fee_details'),
    path('hostel_fee_receipts/', hostel_fee_receipts_view, name='hostel_fee_receipts'),
    path('edit-student/<int:student_id>/', edit_student, name='edit_student'),
    path('course_list', course_list, name='course_list'),
    path('course_list/<str:course_name>/', student_list, name='student_list'),  # Fixed path name
    path('course_list/<str:course_name>/add_mark/<str:student_id>/', add_mark, name='add_mark'),  
    path('view_marks/', view_marks, name='view_marks'),# Ensure this matches the view
    path('examinations/', examinations_dashboard, name='examinations_dashboard'),
    path('examinations/add/', add_exam_result, name='add_exam_result'),
    path('subcourses/', subcourse_list, name='subcourse_list'),
    path('subcourses/<int:subcourse_id>/add_subject/', add_subject, name='add_subject'),
    path('usermark/', usermark, name='usermark'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('view_attendance/', view_attendance, name='view_attendance'),
    path('upload_material/', upload_material, name='upload_material'),
    path('materials/', view_materials, name='view_materials'),
    path('mark_notifications_read/', mark_notifications_read, name='mark_notifications_read'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),
    path('delete_subject/<int:subject_id>/', delete_subject, name='delete_subject'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),
    path('delete_fee_receipt/<int:receipt_id>/', delete_fee_receipt, name='delete_fee_receipt'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
