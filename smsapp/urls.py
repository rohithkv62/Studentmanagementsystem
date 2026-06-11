from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *  # This imports all views from views.py

from .views import edit_student

urlpatterns = [
    path('add_user/', add_user, name='add_user'),
    path('add_course/', add_course, name='add_course'),
    path('', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('landing/', landing_page, name='landing_page'),
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
    path('subcourses/', subcourse_list, name='subcourse_list'),
    path('subcourses/<int:subcourse_id>/add_subject/', add_subject, name='add_subject'),
    path('usermark/', usermark, name='usermark'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
