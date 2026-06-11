from django import forms
from .models import HostelFeeDetails, StudentDetails, Course
class FeeReceiptForm(forms.ModelForm):
    class Meta:
        model = HostelFeeDetails
        fields = ['fee_receipt']

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = '__all__'
        widgets = {
            'course_name': forms.Select(),  # This ensures a dropdown is used for ForeignKey
        }
