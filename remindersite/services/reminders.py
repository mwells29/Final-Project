from datetime import timedelta
from django.utils import timezone
from remindersite.models import Student

REMINDER_DAYS = (90, 60, 30)

def get_iep_reminder_dates(iep_date):
    return {days: iep_date - timedelta(days=days) for days in REMINDER_DAYS}

def get_upcoming_reminders(today=None):
    today = today or timezone.localdate()
    reminders = []
    for student in Student.objects.exclude(iep_date__isnull=True).order_by("iep_date", "name"):
        days_until_iep = (student.iep_date - today).days
        if days_until_iep < -90:
            continue
        for days, reminder_date in get_iep_reminder_dates(student.iep_date).items():
            if today <= reminder_date <= today + timedelta(days=90):
                reminders.append({"student": student, "days_before": days, "reminder_date": reminder_date, "days_until_iep": days_until_iep,})
    return sorted(reminders, key=lambda item: item["student"].iep_date)