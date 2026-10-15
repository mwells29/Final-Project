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
            pass
        raise ValueError(f"Invalid date: {value!r} entered")

def _grade(value):
    mapping = {"freshman": "FR", "fr": "FR", "sophomore": "SO", "so": "SO",
               "junior": "JR", "jr": "JR", "senior": "SR", "sr": "SR"}
    result = mapping.get(str(value or "").strip().lower())
    if not result:
        raise ValueError(f"Unrecognized grade: {value!r}")
    return result

@transaction.atomic
def import_students_from_excel(uploaded_file):
    workbook = load_workbook(uploaded_file, read_only=true, data_only=True)
    sheet = workbook.active
    imported = 0
    try:
        for row_number, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not row or not row[0]:
                continue
            values = list(row) + [None] * max(0, 15 - len(row))
            raw_disability = values[12]
            if isinstance(raw_disability, (list, tuple, set)):
                disability = list(raw_disability)
            elif raw_disability in (None, ""):
                disability = ["None"]
            else:
                disability = [part.strip() for part in str(raw_disability).replace(";", ",").split(",") if part.strip()]
                valid_disabilites = {value for value, _label in Student.DISABILITY_CHOICES}
                disability = [item for item in disability if item in valid_disabilites] or ["None"]
                raw_grade = values[1]
                raw_resources = str(values[6] or "None").strip()
                valid_resources = {value for value, _label in Student.RESOURCE_CHOICES}
                raw_needs = str(value[11] or "None").strip()
                valid_needs = {value for value, _lablel in Student.NEEDS_CHOICES}
                Student.objects.create(
                    name=str(values[0]).strip(),
                    grade=_grade(raw_grade),
                    current_tor=str(values[2] or "").strip(),
                    iep_date=_clean_date(values[3]),
                    scheduled=_clean_date(values[4]),
                    former_tor=str(values[5] or "").strip(),
                    resources=raw_resources if raw_resources in valid_resources else "None",
                    notes=str(values[7] or ""),
                    teacher_email=str(values[8] or "").strip(),
                    update_skyward=str(values[9] or "").strip().lower() in ("true", "yes", "1", "y"),
                    onlines_classes=str(values[10] or "").strip().lower() in ("true", "yes", "1", "y"),
                    needs=raw_needs if raw_needs in valid_needs else "None",
                    lre=int(values[12]) if values[12] not in (None, "") else None,
                    disability=disability,
                    parent_email=str(values[14] or "").strip(),
                )
                imported += 1
    except Exception as error:
        raise ValueError(f"Problem at Excel row {row_number}: {error}") from error
    finally:
        workbook.close()
    return imported