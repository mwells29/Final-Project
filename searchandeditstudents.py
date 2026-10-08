import openpyxl
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta


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
            print(f"Found student: {student['name']} - Grade: {student['grade']}")
#or no matches
    if not matching_students:
        print(f"Student '{search_name}' not found.")
        return
#single match
    if len(matching_students) == 1:
        student_to_edit = matching_students[0]
        print(f"\nEditing student: {student_to_edit['name']} - Grade: {student_to_edit['grade']}")
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

#get selected student
student = matching_students[choice - 1]

#now display student info
print("Student Information")
fields = list(student.keys())
for i, field in enumerate(fields, start=1):
    field = fields[i]
    print(i+1, ".", field, ":", student[field] )

#what field to edit
field_choice = input("Enter the number of the field to edit (or 'q' to cancel): ")
try:
    field_choice = int(field_choice)
    if field_choice < 1 or field_choice > len(fields):
        print("Invalid field number. Edit operation canceled.")
        return
    except ValueError:
    print("Please enter a number corresponding to the field you want to edit.")
    return
if field_choice.lower() == 'q':
    print("Edit operation canceled.")
    return
 #update field
field = fields[field_choice - 1]
new_value = input(f"Enter the new value for {field} (current value: {student[field]}): ")
student[field] = new_value      
print(f"{field} updated successfully for {student['name']}.")

#main menu
def main():

    students, workbook_file = import_excel_file()
    if students is None:
        print("No students loaded. Exiting.")
        return
    while True:
        print("\nStudent Management Menu:")
        print("1. View all students")
        print("2. Search for a student by name")
        print("3. Edit a student's information")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_students(students)
        elif choice == '2':
            search_student(students, input("Enter the name of the student to search: "))
        elif choice == '3':
            edit_student(students)
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

#IEP Reminder
from datetime import datetime,timedelta

def get_iep_reminder_dates(iep_date):
    """
    Given an IEP date, return a list of reminder dates.
    Reminder dates are 30, 60, and 90 days before the IEP date.
    """
    reminder_dates = []
    for days_before in [30, 60, 90]:
        reminder_date = iep_date - timedelta(days=days_before)
        reminder_dates.append(reminder_date)
    return reminder_dates

def check_iep_reminders(students):
    """
    Check each student's IEP date and print reminders if the IEP date is within 30, 60, or 90 days.
    """
    today = datetime.now().date()
    for student in students:
        iep_date = student.get("iep_date")
        if iep_date:
            reminder_dates = get_iep_reminder_dates(iep_date)
            for reminder_date in reminder_dates:
                if today == reminder_date:
                    print(f"Reminder: {student['name']}'s IEP is needing to be scheduled for no later than {iep_date}. Please reach out to the 
                          student's Teacher of Record to schedule the IEP meeting.")    

def send_iep_email(student, reminder_date):
    """
    Send an email reminder for the student's IEP.
    This is a placeholder function. Implement email sending logic here.
    """
   parent_email = student.get("parent_email")
   teacher_email = student.get("teacher_email")
   student_name = student.get("name")
   iep_date = student.get("iep_date")

   subject = f"IEP Reminder for {student_name}"
   message = f"Hello,\n\nThis is a reminder that {student_name]'s '

   
#start program
main()