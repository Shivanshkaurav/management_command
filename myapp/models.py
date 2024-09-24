from django.db import models

class Student(models.Model):
    name = models.CharField(default=" ",max_length=200, blank=False, null=False)
    roll = models.PositiveIntegerField(unique=True)
    date_of_birth = models.DateField()
    home_address = models.CharField(max_length=200, default=" ")
    def __str__(self):
        return self.name