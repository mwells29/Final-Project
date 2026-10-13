from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "name",
            "grade",
            "iep_date",
            "parent_email",
            "teacher_email",
            "scheduled",
            "notes",
        ]