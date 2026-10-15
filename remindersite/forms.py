from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "name",
            "grade",
            "iep_date",
            "scheduled",
            "former_tor",
            "current_tor",
            "resource",
            "parent_email",
            "teacher_email",
            "scheduled",
            "notes",
            "update_skyward",
            "online_classes",
            "needs",
            "disability",
            "lre",
        ]

        widgets = {
            "iep_date": forms.DateInput(attrs={"type": "date"}),
            "scheduled": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label="Select an Excel file in .xlsx format", required=True)

    def clean_excel_file(self):
        uploaded_file = self.cleaned_data.get("excel_file")
        if not uploaded_file.name.endswith(".xlsx"):
            raise forms.ValidationError("Please upload a valid Excel file in .xlsx format.")
        return uploaded_file 

    