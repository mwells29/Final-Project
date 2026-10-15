from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from.forms import StudentForm, ExcelImportForm
from .models import Student
from.services.excel_service import import_students_from_excel
from.services.reminders import send_reminders


def dashboard(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all().order_by("name")
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(grade__icontains=query) 
        )
    return render(request, 'dashboard.html', 
                      {"students": students, 
                       "query": query,
                       "student_count": Student.objects.count(),
                       "remidners": get_upcoming_reminders(),
                       "import_form": ExcelImportForm(),})
        
#get student detail view
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_detail.html', {"student": student})

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
    if request.method == "POST":
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            import_students_from_excel(excel_file)
            messages.success(request, "Students imported successfully.")
            return redirect("dashboard")
    else:
        form = ExcelImportForm()
    return render(request, "remindersite/import_excel.html", {"form": form})