from django import forms
from .models import Course

class CourseForm(forms.ModelForm):

    class Meta:

        model = Course
        fields = '__all__'
        widgets = {
            'course_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Course Name'}),
            'trainer': forms.Select(attrs={'class':'form-control','placeholder':'Choose Trainer'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter the price'}),
        }