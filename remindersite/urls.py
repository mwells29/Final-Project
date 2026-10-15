
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:student_id>/", views.student_detail, name="student_detail"),
    path("students/<int:student_id>/edit/", views.edit_student, name="edit_student"),
    path("students/import/", views.import_excel, name="import_excel"),
]