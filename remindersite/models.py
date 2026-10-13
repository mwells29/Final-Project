from django.db import models
from multiselectfield import MultiSelectField


class Student(models.Model):
    name = models.CharField(max_length=200,
        null=False,
        blank=False
    )

    GRADE_CHOICES = [
        ("FR", "Freshman"),
        ("SO", "Sophomore"),
        ("JR", "Junior"),
        ("SR", "Senior"),
    ]
    grade = models.CharField(max_length=20,
        null=False,
        blank=False,
        choices=GRADE_CHOICES       
    )

    iep_date = models.DateField(
        null=True,
        blank=True
    )
 
    scheduled = models.DateField(
        null=True,
        blank=True
    )

    former_tor = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    RESOURCE_CHOICES = [
        ("Wells", "Wells"),
        ("Rossman", "Rossman"),
        ("Walters", "Walters"),
        ("Brink", "Brink"),
        ("White", "White"),
        ("Socks", "Socks"),
        ("Waalkens", "Waalkens"),
        ("Wilson", "Wilson"),
        ("Consult", "Consult"),
        ("None","None"),
    ]
    resource = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=RESOURCE_CHOICES
    )

    notes = models.TextField(
        blank=True
    )
 
    teacher_email = models.EmailField(
        blank=False
    )

    update_skyward = models.BooleanField(
        default=False   
    )

    online_classes = models.BooleanField(
        default=False       
    )   

    NEEDS_CHOICES = [
        ("None", "None"),
        ("Write", "Write"),
        ("Schedule", "Schedule"),
        ("Update", "Update"),
        ("Done", "Done")
    ]

    needs = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        choices=NEEDS_CHOICES
    )

    lre = models.IntegerField(
        null=True,
        blank=True
    )   

    DISABILITY_CHOICES = [
        ("None", "None"),
        ("SLD", "SLD"),
        ("OHI", "OHI"),
        ("Speech", "Speech"),
        ("Emotional", "Emotional"),
        ("Intellectual", "Intellectual"),
        ("Autism", "Autism"),
        ("Hearing", "Hearing"),
        ("Visual", "Visual"),
        ("Orthopedic", "Orthopedic"),
        ("TBI", "TBI"),
        ("Deaf-Blindness", "Deaf-Blindness"),
    ]       

    disability = MultiSelectField(
        choices=DISABILITY_CHOICES,
        max_choices=11,
        null=False,
        blank=False
    )
    def __str__(self):
        return self.name