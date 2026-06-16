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
    if request.method == 'POST':
        course_name = request.POST['course_name']

        # Check if the course name already exists
        if Course.objects.filter(name=course_name).exists():
            error_message = "Course name already exists."
            return render(request, 'addcourse.html', {'error_message': error_message})
        
        # Create the course
        Course.objects.create(name=course_name)
        success_message = "Course added successfully!"
        return render(request, 'addcourse.html', {'success_message': success_message})

    return render(request, 'addcourse.html')

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
    context = {}
    if request.user.is_superuser:
        context['total_students'] = StudentDetails.objects.count()
        context['total_courses'] = Course.objects.count()
        context['pending_leaves'] = LeaveRequest.objects.filter(status='Pending').count()
        context['total_feedback'] = Feedback.objects.count()
    else:
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
    if request.method == 'POST':
        subject = request.POST['subject']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        status = 'Pending'

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
        except StudentDetails.DoesNotExist:
            messages.error(request, "Student details not found.")
        
        return redirect('add_leave_request')

    return render(request, 'add_leave_request.html')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

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
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Leave request not found.")
        
        return redirect('view_leave_requests')
    
    leave_requests = LeaveRequest.objects.all()
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


