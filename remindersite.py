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
            number += 1

#search for a student by name
def search_student(students, name):
    search_name = input("Enter the name of the student to search: ")
    search_name = search_name.strip().lower()
    
    print(f"\nSearching for student: {search_name}")


    for student in students:
        if student["name"].lower() == search_name:
            print("\nStudent found:")
            for key, value in student.items():
                print(f"{key}: {value}")
            return student
    print(f"Student '{search_name}' not found.")
    return None

#edit student
def edit_student(students):
    search_name = input("Enter the name of the student to edit: ")
    search_name = search_name.strip().lower()
   
    matching_students = []

#find students with the same name
    for student in students:
        if student["name"].lower() == search_name:
            matching_students.append(student)

#or no matches
    if not matching_students:
        print(f"Student '{search_name}' not found.")
        return
#single match
    if len(matching_students) == 1:
        student_to_edit = matching_students[0]
    else:
#multiple matches
   print(f"\nMultiple students found with the name '{search_name}':")

   for i, student in enumerate(matching_students, start=1):
       print(f"{i}. {student['name']} - Grade: {student['grade']}")

    choice = input("Enter the number of the student to edit or 'q' to cancel: ")
    if choice.lower() == 'q':
        print("Edit operation canceled.")
        return
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(matching_students):
            print("Invalid choice. Edit operation canceled.")
            return

        student_to_edit = matching_students[index]

    except ValueError:
        print("Invalid input. Edit operation canceled.")
        return

print(f"\nEditing student: {student_to_edit['name']}, Grade: {student_to_edit['grade']}")

    