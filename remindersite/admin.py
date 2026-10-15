from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade",
        "iep_date",
        "scheduled",
        "former_tor",
        "current_tor",
        "resource",
        "parent_email",
        "teacher_email",
        "notes",
        "update_skyward",
        "online_classes",
        "needs",
        "disability",
        "lre",
    )
    list_filter = ("name", "grade", "resource", "disability", "iep_date", "current_tor")
    search_fields = ("name", "grade", "resource", "disability", "iep_date", "current_tor")
# Register your models here.
