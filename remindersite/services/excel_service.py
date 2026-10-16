from datetime import datetime, date
from openpyxl import load_workbook
from django.db import transaction
from remindersite.models import Student

def _clean_date(value):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    for fmt in ("%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date: {value!r} entered")

def _grade(value):
    mapping = {"freshman": "FR", "fr": "FR", "sophomore": "SO", "so": "SO",
               "junior": "JR", "jr": "JR", "senior": "SR", "sr": "SR"}
    result = mapping.get(str(value or "").strip().lower())
    if not result:
        raise ValueError(f"Unrecognized grade: {value!r}")
    return result

def _choice(value, choices, field_name, default=None):
    valid_values = {choice[0] for choice in choices}
    cleaned = str(value or "").strip()
    if not cleaned and default is not None:
        return default
    choices_by_lowercase = {
        str(choice).lower:choice
        for choice in valid_values
    }

    matched = choices_by_lowercase.get(cleaned.lower())

    if matched is None:
        raise ValueError(
            f"Invalid {field_name}: {cleaned!r}. "
            f"Allowed values: {', '.join(sorted(valid_values))}"
        )
        
    return matched

@transaction.atomic
def import_students_from_excel(uploaded_file):
    workbook = load_workbook(uploaded_file, read_only=True, data_only=True)
    imported = 0
    row_number = 1
    
    try:
        #this makes it look for the first sheet rather than active sheet
        if "Sheet1" not in workbook.sheetnames:
            raise ValueError("The workbook does not contain a worksheet named Sheet1.")

        sheet=workbook["Sheet1"]
        
        for row_number, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not row or not row[0]:
                continue
            values = list(row) 
            values.extend([None] * max(0, 15 - len(values)))

            name = str(values[0]).strip()
            grade = _grade(values[1])

            current_tor = values[2]
            if current_tor not in (None, ""):
                current_tor = _choice(
                    current_tor, 
                    Student.TOR_CHOICES, 
                    "Current TOR"
                )
            else:
                current_tor = None

            
            iep_date = _clean_date(values[3])
            
            scheduled = _clean_date(values[4])
            
            former_tor = str(values[5] or "").strip()
                        
            resource = _choice(
                    values[6],
                    Student.RESOURCE_CHOICES,
                    "Resource",
                    default="None"
                )

            notes = str(values[7] or "")

            teacher_email = str(values[8] or "").strip()
            if not teacher_email:
                raise ValueError("Teacher email is required")            

            update_skyward = (
                str(values[9] or "").strip().lower()
                in ("true", "yes", "1", "y")
            )

            online_classes = (
                str(values[10] or "").strip().lower()
                in ("true", "yes", "1", "y")
            )
            
            needs = _choice(
                values[11],
                Student.NEEDS_CHOICES,
                "needs",
                default="None",
            )

            raw_lre = values[12]
            lre = int(raw_lre) if raw_lre not in (None, "") else None

            raw_disability = values[13]
            
            if isinstance(raw_disability, (list, tuple, set)):
                disability = list(raw_disability)
            elif raw_disability in (None, ""):
                disability = ["None"]
            else:
                disability = [
                    part.strip()
                    for part in str(raw_disability).replace(";", ",").split(",") 
                    if part.strip()
                ]
                
            valid_disabilities = {
                value for value, _label in Student.DISABILITY_CHOICES
            }
                
            disability = [
                item for item in disability if item in valid_disabilities
            ] or ["None"]
                
            parent_email = str(values[14] or "").strip() or None
             
            Student.objects.create(
                name=name,
                grade=grade,
                current_tor=current_tor,
                iep_date=iep_date,
                scheduled=scheduled,
                former_tor=former_tor,
                resource=resource,
                notes=notes,
                teacher_email=teacher_email,
                update_skyward=update_skyward,
                online_classes=online_classes,
                needs=needs,
                lre=lre,
                disability=disability,
                parent_email=parent_email,
             )
            imported += 1
    except Exception as error:
        raise ValueError(f"Problem at Excel row {row_number}: {error}") from error
    finally:
        workbook.close()
    return imported