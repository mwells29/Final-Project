import openpyxl
from tkinter import Tk
from tkinter.filedialog import askopenfilename



#let's import the excel file
filename = askopenfilename(
    title="Please select your caseload file to import",
    filetypes=[("Excel files", "*.xlsx")],
)  

if not filename:
    print("No file selected. Exiting.")
    exit()

try: 
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    students = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        student = {
            "name": row[0],
            "grade": row[1],
            "iep_date": row[2],
            "scheduled": row[3],
            "former_tor": row[4],
            "resource": row[5],
            "notes": row[6],
            "current_tor": row[7],
            "teacher_email": row[8],
            "update_skyware": row[9],
            "online_classes": row[10],
            "needs": row[11],
            "lre": row[12],
            "disability": row[13],
            "parent_email": row[14],
        }
        students.append(student)
    print(f"\n{len(students)} students loaded from Excel file.")
    print("\nExcel file loaded successfully.")

except Exception as e:
    print(f"Error occurred while loading the Excel file: {e}")
    exit()

#view all students
def view_students(students):
    print("\nStudent List:")
    for student in students:
        print(f"Name: {student['name']}, 
              Grade: {student['grade']}, 
              IEP Date: {student['iep_date']}, 
              Scheduled: {student['scheduled']}, 
              Former TOR: {student['former_tor']}, 
              Resource: {student['resource']}, 
              Notes: {student['notes']}, 
              Current TOR: {student['current_tor']}, 
              Teacher Email: {student['teacher_email']}, 
              Update Skyware: {student['update_skyware']}, 
              Online Classes: {student['online_classes']}, 
              Needs: {student['needs']}, LRE: {student['lre']}, 
              Disability: {student['disability']}, 
              Parent Email: {student['parent_email']}")
