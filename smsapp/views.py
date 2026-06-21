from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Course, StudentDetails, Feedback, LeaveRequest, HostelFeeDetails,StudentFeeReceipt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import FeeReceiptForm, StudentForm
from .models import Subject, Course




def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists."
            return render(request, 'adduser.html', {'error_message': error_message})
        
        # Create the user
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'User added successfully!')
        return redirect('add_user')

    return render(request, 'adduser.html')

def add_course(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        course_name = request.POST['course_name']

        # Check if the course name already exists
        if Course.objects.filter(name=course_name).exists():
            error_message = "Course name already exists."
            return render(request, 'addcourse.html', {'error_message': error_message, 'courses': courses})
        
        # Create the course
        Course.objects.create(name=course_name)
        success_message = "Course added successfully!"
        return render(request, 'addcourse.html', {'success_message': success_message, 'courses': Course.objects.all()})

    return render(request, 'addcourse.html', {'courses': courses})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')  # Redirect to the landing page after successful login
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists."
            return render(request, 'signup.html', {'error_message': error_message})
        
        # Create the user
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Signup successful! Please login.')
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def landing_page(request):
    from .models import TeacherProfile, StudyMaterial
    
    # Auto-fix any existing teachers that don't have is_staff=True
    if hasattr(request.user, 'teacher_profile') and not request.user.is_staff:
        request.user.is_staff = True
        request.user.save()

    context = {}
    if request.user.is_superuser:
        context['total_students'] = StudentDetails.objects.count()
        context['total_courses'] = Course.objects.count()
        context['pending_leaves'] = LeaveRequest.objects.filter(status='Pending').count()
        context['total_feedback'] = Feedback.objects.count()
    elif request.user.is_staff:
        # Teacher Dashboard context
        context['total_students'] = StudentDetails.objects.count()
        context['total_courses'] = Course.objects.count()
        context['study_materials'] = StudyMaterial.objects.count()
    else:
        # Student Dashboard context
        student_details = StudentDetails.objects.filter(username=request.user).first()
        context['student_details'] = student_details
        if student_details:
            context['my_leaves'] = LeaveRequest.objects.filter(student_name=student_details).count()
            context['my_pending_leaves'] = LeaveRequest.objects.filter(student_name=student_details, status='Pending').count()
            context['fee_details'] = HostelFeeDetails.objects.filter(student=student_details).first()
        else:
            context['my_leaves'] = 0
            context['my_pending_leaves'] = 0
            context['fee_details'] = None
            
    return render(request, 'landing_page.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def add_student(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        course_id = request.POST.get('course_name')
        scholarship = request.POST.get('scholarship')
        admission_date = request.POST.get('admission_date')
        admission_number = request.POST.get('admission_number')
        hosteler = request.POST.get('hosteler')  # Convert checkbox value to boolean
        
        

        try:
            course = Course.objects.get(id=int(course_id))
        except (ValueError, Course.DoesNotExist):
            error_message = "Invalid course selected."
            return render(request, 'add_student.html', {
                'error_message': error_message,
                'courses': Course.objects.all()
            })

        user = request.user

        student, created = StudentDetails.objects.update_or_create(
            admission_number=admission_number,
            defaults={
                'username': user,
                'full_name': full_name,
                'father_name': father_name,
                'mother_name': mother_name,
                'age': age,
                'gender': gender,
                'address': address,
                'course_name': course,
                'scholarship': scholarship,
                'admission_date': admission_date,
                'hosteler': hosteler,
            }
        )

        success_message = "Student details added successfully!" if created else "Student details updated successfully!"
        
        # Notify admins
        from .models import Notification
        Notification.objects.create(message=f"New student {'added' if created else 'updated'}: {full_name}")

        return render(request, 'add_student.html', {
            'success_message': success_message,
            'courses': Course.objects.all()
        })

    courses = Course.objects.all()
    return render(request, 'add_student.html', {
        'courses': courses
    })

def add_feedback(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        try:
            student = StudentDetails.objects.get(username=request.user)
            Feedback.objects.create(student_name=student, title=title, content=content)
            messages.success(request, "Feedback submitted successfully!")
        except StudentDetails.DoesNotExist:
            messages.error(request, "Student details not found.")
        
        return redirect('add_feedback')

    return render(request, 'add_feedback.html')

def add_leave_request(request):
    from django.utils import timezone
    if request.method == 'POST':
        subject = request.POST['subject']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        status = 'Pending'

        if request.user.is_staff and not request.user.is_superuser:
            # Teacher applying for leave
            first_course = Course.objects.first()
            student, _ = StudentDetails.objects.get_or_create(
                username=request.user,
                defaults={
                    'full_name': f"{request.user.first_name} {request.user.last_name} (Teacher)",
                    'father_name': 'N/A',
                    'mother_name': 'N/A',
                    'age': 30,
                    'gender': 'N/A',
                    'address': 'N/A',
                    'course_name': first_course,
                    'admission_date': timezone.now().date(),
                    'admission_number': f"T_{request.user.id}"
                }
            )
            LeaveRequest.objects.create(
                student_name=student,
                subject=subject,
                from_date=from_date,
                to_date=to_date,
                status=status
            )
            messages.success(request, "Teacher leave request submitted successfully!")
            from .models import Notification
            Notification.objects.create(message=f"New teacher leave request submitted by {student.full_name}")
        else:
            try:
                student = StudentDetails.objects.get(username=request.user)
                LeaveRequest.objects.create(
                    student_name=student,
                    subject=subject,
                    from_date=from_date,
                    to_date=to_date,
                    status=status
                )
                messages.success(request, "Leave request submitted successfully!")
                
                # Notify admins
                from .models import Notification
                Notification.objects.create(message=f"New leave request submitted by {student.full_name}")
            except StudentDetails.DoesNotExist:
                messages.error(request, "Student details not found.")
        
        return redirect('add_leave_request')

    return render(request, 'add_leave_request.html')

def courses(request):
    subjects = Subject.objects.all()
    courses_list = Course.objects.all()
    
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        semester = request.POST.get('semester')
        course_id = request.POST.get('course_id')

        if subject_name and subject_code and semester and course_id:
            course = get_object_or_404(Course, id=course_id)
            Subject.objects.create(
                course_name=course.name,
                subject_name=subject_name,
                subject_code=subject_code,
                semester=semester
            )
            messages.success(request, "Subject added successfully!")
            return redirect('courses')
        else:
            messages.error(request, "Please fill all fields.")
            
    return render(request, 'course_list.html', {'subjects': subjects, 'courses_list': courses_list})

def course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = StudentDetails.objects.filter(course_name=course)
    return render(request, 'course_students.html', {'course': course, 'students': students})

def feedback_list(request):
    feedbacks = Feedback.objects.all().select_related('student_name')
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

def view_leave_requests(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        
        try:
            leave_request = LeaveRequest.objects.get(id=request_id)
            leave_request.status = 'Approved' if action == 'approve' else 'Denied'
            leave_request.save()
            messages.success(request, "Leave request updated successfully!")
            
            # Notify the student
            from .models import Notification
            Notification.objects.create(
                user=leave_request.student_name.username,
                message=f"Your leave request for '{leave_request.subject}' was {leave_request.status}."
            )
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Leave request not found.")
        
        return redirect('view_leave_requests')
    
    if request.user.is_superuser:
        leave_requests = LeaveRequest.objects.all().order_by('-id')
    else:
        # Teachers only see student leave requests
        leave_requests = LeaveRequest.objects.exclude(student_name__admission_number__startswith="T_").order_by('-id')
        
    return render(request, 'view_leave_requests.html', {'leave_requests': leave_requests})

from django.shortcuts import render
from .models import StudentDetails, LeaveRequest

def student_leave_status(request):
    try:
        # Use filter() to get all student details associated with the user
        student_details = StudentDetails.objects.filter(username=request.user)
        
        if student_details.exists():
            # Get the first StudentDetails entry if multiple exist
            student = student_details.first()

            # Retrieve leave requests for the selected student
            leave_requests = LeaveRequest.objects.filter(student_name=student)
            
            return render(request, 'status_leave.html', {'leave_requests': leave_requests})
        else:
            # Handle case when no student details are found for the user
            return render(request, 'status_leave.html', {'error_message': 'Student details not found.'})
    
    except Exception as e:
        # Handle any other unexpected exceptions
        return render(request, 'status_leave.html', {'error_message': f'An error occurred: {str(e)}'})




@login_required
def hostel_fee_details(request):

    try:
        # Fetch the student details for the logged-in user
        student_details = StudentDetails.objects.filter(username=request.user).first()
        if not student_details:
            return render(request, 'hostel_fee_details.html', {'error_message': 'Student details not found.'})

        # Fetch or create the hostel fee details for the student
        hostel_fee_details, created = HostelFeeDetails.objects.get_or_create(
            student=student_details,
            defaults={'fee_amount': 0.00}
        )

    except StudentDetails.DoesNotExist:
        return render(request, 'hostel_fee_details.html', {'error_message': 'Student details not found.'})

    if request.method == 'POST':
        form = FeeReceiptForm(request.POST, request.FILES, instance=hostel_fee_details)
        if form.is_valid():
            hostel_fee_details = form.save(commit=False)
            hostel_fee_details.save()
            # Create a new StudentFeeReceipt entry
            StudentFeeReceipt.objects.create(
                student=student_details,
                receipt_file=hostel_fee_details.fee_receipt,
                fee_amount=hostel_fee_details.fee_amount
            )
            messages.success(request, "Receipt uploaded successfully!")
            
            # Notify admins
            from .models import Notification
            Notification.objects.create(message=f"Hostel fee receipt uploaded by {student_details.full_name}")
            
            return redirect('hostel_fee_details')
    else:
        form = FeeReceiptForm(instance=hostel_fee_details)

    context = {
        'student_details': student_details,
        'form': form,
        'receipt': hostel_fee_details  # Pass the receipt to the template
    }
    return render(request, 'hostel_fee_details.html', context)

@login_required
def hostel_fee_receipts_view(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect to home if not superuser

    receipts = StudentFeeReceipt.objects.select_related('student').all()  # Fetch all receipts with related student details

    return render(request, 'hostel_fee_receipts.html', {'receipts': receipts})






def edit_student(request, student_id):
    student = get_object_or_404(StudentDetails, id=student_id)  # Use StudentDetails instead of Student
    courses = Course.objects.all()  # Fetch all courses
    
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('course_students', course_id=student.course_name.id)
        else:
            print(form.errors)  # Debugging line to check form errors
            messages.error(request, "There were errors in the form. Please check the inputs.")

    else:
        form = StudentForm(instance=student)
    
    return render(request, 'edit_student.html', {'form': form, 'student': student, 'courses': courses  } )

@login_required
def delete_course(request, course_id):
    if request.user.is_superuser:
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        messages.success(request, "Course deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'landing_page'))

@login_required
def delete_subject(request, subject_id):
    if request.user.is_superuser:
        subject = get_object_or_404(Subject, id=subject_id)
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'landing_page'))

@login_required
def delete_teacher(request, teacher_id):
    if request.user.is_superuser:
        teacher = get_object_or_404(TeacherProfile, id=teacher_id)
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'landing_page'))

@login_required
def delete_student(request, student_id):
    if request.user.is_superuser:
        student = get_object_or_404(StudentDetails, id=student_id)
        student.delete()
        messages.success(request, "Student deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'landing_page'))

@login_required
def delete_fee_receipt(request, receipt_id):
    if request.user.is_superuser:
        receipt = get_object_or_404(StudentFeeReceipt, id=receipt_id)
        receipt.delete()
        messages.success(request, "Fee receipt deleted successfully.")
    return redirect(request.META.get('HTTP_REFERER', 'landing_page'))

from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Subject

def subcourse_list(request):
    subcourses = Course.objects.all()  # Assuming Course model still stores the subcourse data
    return render(request, 'subcourse_list.html', {'subcourses': subcourses})

def add_subject(request, subcourse_id):
    subcourse = get_object_or_404(Course, pk=subcourse_id)

    if request.method == 'POST':
        # Retrieve the data from the form
        subject_names = request.POST.getlist('subject_name')
        subject_codes = request.POST.getlist('subject_code')
        semesters = request.POST.getlist('semester')

        # Iterate over the submitted subjects
        for name, code, semester in zip(subject_names, subject_codes, semesters):
            if name and code and semester:  # Ensure all fields are filled
                # Create and save each subject
                Subject.objects.create(
                    course_name=subcourse,
                    subject_name=name,
                    subject_code=code,
                    semester=semester
                )
        return redirect('subcourse_list')
    
    return render(request, 'add_subject.html', {'subcourse': subcourse})



from django.shortcuts import render, redirect
from .models import Course, StudentDetails, Subject, Mark

# View for the course list
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courselist.html', {'courses': courses})

# View for the student list
def student_list(request, course_name):
    students = StudentDetails.objects.filter(course_name__name=course_name)
    return render(request, 'student_list.html', {'students': students, 'course_name': course_name})

# View for adding marks
def add_mark(request, course_name, student_id):
    if request.method == 'POST':
        subjects = request.POST.getlist('subject')  # Get all selected subjects
        marks = request.POST.getlist('marks')  # Get corresponding marks

        for subject_id, mark in zip(subjects, marks):
            if subject_id and mark:  # Ensure both subject and mark are provided
                Mark.objects.create(student_id=student_id, subject_id=subject_id, marks_obtained=mark)

        return redirect('student_list', course_name=course_name)  # Redirect back to student list

    subjects = Subject.objects.all()  # Get all subjects for the dropdown
    return render(request, 'addmark.html', {
        'subjects': subjects,
        'student_id': student_id,
    })

def view_marks(request):
    marks = None  # Initialize marks variable to hold the results
    msg = None  # Initialize msg to avoid UnboundLocalError

    if request.method == "POST":
        admission_number = request.POST.get('admission_number')
        semester = int(request.POST.get('semester'))  # Convert semester to an integer

        # Fetch the student's marks based on admission_number and semester
        try:
            student = StudentDetails.objects.get(admission_number=admission_number)
            marks = Mark.objects.filter(student=student, subject__semester=semester).select_related('subject')

            # Check if all marks are <= 50.0
            if marks.exists() and all(mark.marks_obtained <= 50.0 for mark in marks):
                msg = "Failed"
            else:
                msg = "Passed"
        except StudentDetails.DoesNotExist:
            marks = []  # No marks if student doesn't exist
            msg = "Student not found."  # Add an appropriate message for the exception

    return render(request, 'view_marks.html', {'marks': marks, 'msg': msg})

@login_required
def examinations_dashboard(request):
    marks = Mark.objects.all().select_related('student', 'subject')
    
    # Filtering logic
    course_filter = request.GET.get('course')
    subject_filter = request.GET.get('subject')
    student_filter = request.GET.get('student')
    
    if course_filter:
        marks = marks.filter(subject__course_name__icontains=course_filter)
    if subject_filter:
        marks = marks.filter(subject__subject_name__icontains=subject_filter)
    if student_filter:
        marks = marks.filter(student__full_name__icontains=student_filter)
        
    context = {
        'marks': marks,
        'course_filter': course_filter,
        'subject_filter': subject_filter,
        'student_filter': student_filter,
    }
    return render(request, 'examinations_dashboard.html', context)

@login_required
def add_exam_result(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        marks_obtained = request.POST.get('marks')
        
        if student_id and subject_id and marks_obtained:
            Mark.objects.create(
                student_id=student_id, 
                subject_id=subject_id, 
                marks_obtained=marks_obtained
            )
            messages.success(request, 'Exam result added successfully!')
            return redirect('examinations_dashboard')
            
    students = StudentDetails.objects.all().order_by('full_name')
    subjects = Subject.objects.all().order_by('subject_name')
    return render(request, 'add_exam_result.html', {'students': students, 'subjects': subjects})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudentDetails, Mark

@login_required
def usermark(request):
    student_details = StudentDetails.objects.filter(username=request.user)

    if student_details.exists():
        # Get the first student record for the user
        student = student_details.first()

        marks = None
        selected_semester = None
        msg = None  # Initialize msg to avoid UnboundLocalError
        
        if request.method == 'POST':
            selected_semester = request.POST.get('semester')
            # Filter marks for the student by the selected semester
            marks = Mark.objects.filter(student=student, subject__semester=selected_semester)
            
            # Check if all marks are less than or equal to 50.0
            if marks.exists() and all(mark.marks_obtained <= 50.0 for mark in marks):
                msg = "Failed"
            else:
                msg = "Passed"

        return render(request, 'usermark.html', {
            'student': student,
            'marks': marks,
            'selected_semester': selected_semester,
            'msg': msg  # msg is now initialized
        })
    else:
        # Handle case when no student details are found for the user
        return render(request, 'usermark.html', {
            'error': 'No student details found for this user.'
        })


@login_required
def students_page(request):
    # Retrieve all students and courses for the template
    students_list = StudentDetails.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        # Delegate adding a student to add_student view logic or handle it here
        return redirect('students_page')
    return render(request, 'students_page.html', {'students_list': students_list, 'courses': courses})

@login_required
def teachers_page(request):
    from .models import TeacherProfile, Course
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        username = request.POST.get('username')
        password = request.POST.get('password')
        joining_date = request.POST.get('joining_date')
        assigned_class_id = request.POST.get('assigned_class')
        status = request.POST.get('status', 'Present')

        # Split full name into first and last name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True
            )
            
            # Apply joining date if provided
            if joining_date:
                from django.utils.dateparse import parse_datetime
                # Date format from input type="date" is YYYY-MM-DD
                parsed_date = parse_datetime(f"{joining_date} 00:00:00")
                if parsed_date:
                    user.date_joined = parsed_date
                    user.save()

            # Assign class if selected
            course = None
            if assigned_class_id:
                course = Course.objects.filter(id=assigned_class_id).first()

            # Create TeacherProfile
            TeacherProfile.objects.create(
                user=user,
                assigned_class=course,
                status=status
            )
            messages.success(request, f"Teacher {full_name} added successfully.")
            return redirect('teachers_page')

    teachers_list = TeacherProfile.objects.all()
    courses = Course.objects.all()
    return render(request, 'teachers_page.html', {'teachers_list': teachers_list, 'courses': courses})

@login_required
def fee_management_page(request):
    return render(request, 'fee_management_page.html')

@login_required
def hostel_management_page(request):
    return render(request, 'hostel_management_page.html')

@login_required
def mark_attendance(request):
    from .models import Course, StudentDetails, Attendance
    courses = Course.objects.all()
    selected_course = None
    date = None
    students = None

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        date = request.POST.get('date')
        
        if course_id and date:
            course = get_object_or_404(Course, id=course_id)
            students_in_course = StudentDetails.objects.filter(course_name=course)
            
            for student in students_in_course:
                status = request.POST.get(f'status_{student.id}')
                if status:
                    Attendance.objects.update_or_create(
                        course=course,
                        student=student,
                        date=date,
                        defaults={'status': status}
                    )
            messages.success(request, f"Attendance marked for {course.name} on {date}.")
            return redirect('mark_attendance')

    elif request.method == 'GET':
        course_id = request.GET.get('course_id')
        date = request.GET.get('date')
        
        if course_id and date:
            selected_course = get_object_or_404(Course, id=course_id)
            students = StudentDetails.objects.filter(course_name=selected_course)

    return render(request, 'mark_attendance.html', {
        'courses': courses,
        'selected_course': selected_course,
        'date': date,
        'students': students
    })

@login_required
def view_attendance(request):
    from .models import Attendance
    attendances = Attendance.objects.all()
    return render(request, 'view_attendance.html', {'attendances': attendances})

@login_required
def upload_material(request):
    from .models import Course
    courses = Course.objects.all()
    return render(request, 'upload_material.html', {'courses': courses})

@login_required
def view_materials(request):
    from .models import StudyMaterial
    materials = StudyMaterial.objects.all()
    return render(request, 'view_materials.html', {'materials': materials})

@login_required
def mark_notifications_read(request):
    from .models import Notification
    if request.method == 'POST':
        if request.user.is_superuser:
            Notification.objects.filter(user__isnull=True, is_read=False).update(is_read=True)
        else:
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    # Redirect back to where the user came from
    return redirect(request.META.get('HTTP_REFERER', 'landing_page'))
