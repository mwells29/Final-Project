from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from.forms import StudentForm, ExcelImportForm
from .models import Student
from.services.excel_service import import_students_from_excel
from.services.reminders import get_upcoming_reminders
from datetime import date


def dashboard(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all().order_by("name")
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(grade__icontains=query) 
        )
    today = date.today()
    for student in students:
            if student.iep_date:
                student.days_until_iep = (student.iep_date - today).days
            else:
                student.days_until_iep = None

    context = {
        "students": students,
        "query": query,
        "student_count": Student.objects.count(),
        "reminders": get_upcoming_reminders(),
        "import_form": ExcelImportForm(),
    }
    return render(request, 'remindersite/dashboard.html', context)
                      
        
#get student detail view
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'remindersite/student_detail.html', {"student": student})

#create a view for adding a student
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("dashboard")
    else:
        form = StudentForm()
    return render(request, "remindersite/student_form.html", {"form": form, "page_title": "Add Student"})

#create a view for editing a student
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("dashboard")
    else:
        form = StudentForm(instance=student)
    return render(request, "remindersite/student_form.html", {"form": form, "page_title": "Edit Student"})

#create a view for importing students from excel
def import_excel(request):
    if request.method != "POST":
        return redirect("dashboard")
    form = ExcelImportForm(request.POST, request.FILES)
    
    if form.is_valid():
        excel_file = form.cleaned_data["excel_file"]

        try:
            imported_count = import_students_from_excel(excel_file)
            messages.success(request, f"{imported_count} students imported successfully.")
        except Exception as e:
            messages.error(request, f"Error importing excel file: {e}")
    else:
        messages.error(
            request, f"Invalid upload form: {form.errors}"
        )
    return redirect ("dashboard")