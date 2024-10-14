from django import forms
from .models import Course
from .models import Chapter

class CourseForm(forms.ModelForm):

    class Meta:

        model = Course
        fields = '__all__'
        widgets = {
            'course_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the Course Name'}),
            'trainer': forms.Select(attrs={'class':'form-control','placeholder':'Choose Trainer'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter the price'}),
        }

class ChapterForm(forms.ModelForm):

    class Meta:

        model = Chapter
        fields = '__all__'
        widgets = {
            'chapter_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Chapter Name'}),
            
        }