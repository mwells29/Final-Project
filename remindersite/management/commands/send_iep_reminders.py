from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from remindersite.models import Student
from remindersite.services.reminders import get_iep_reminder_dates
from remindersite.services.email_service import send_iep_email



class Command(BaseCommand):
    help = "Send reminders due today to parent and teacher."

    def handle(self, *args, **options):
        today = timezone.localdate()
        sent = 0
        for student in Student.objects.exclude(iep_date_isnull=True).iterator():
            due_days = [days for days, due_date in get_iep_reminder_dates(student.iep_date).items() if due_date == today]
            for days in due_days:
                try:
                    if send_iep_email(student,days):
                        sent += 1
                        self.stdout.write(self.style.SUCCESS(f"Sent {days} day reminder for {student.name}."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Skipped {student.name}: no parent email."))
                except Exception as error:
                    raise CommandError(f"Could not send reminder for student {student.name}: {error}.") from error
        self.stdout.write(self.style.SUCCESS(f"Completed reminder emails. Emails that were sent: {sent}."))
