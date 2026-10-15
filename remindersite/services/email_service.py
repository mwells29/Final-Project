from django.conf import settings
from django.core.mail import EmailMessage


def send_iep_email(student, days_before):
    if not student.parent_email:
        return False
    subject = f"Annual IEP Meeting Reminder for {student.name}"
    message = (
        f"Hello, \n\nThis is a reminder that {student.name}'s annual IEP meeting "
        f"needing to be scheduled for no later than {student.iep_date}. "
        f"Please reach out to {student.current_tor}, the student's current Teacher of Record, to schedule the IEP meeting. \n\n"
        "Thank you."
    )
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[student.parent_email],
        cc=[student.teacher_email] if student.teacher_email else[],
    )
    email.send(fail_silently=False)
    return True