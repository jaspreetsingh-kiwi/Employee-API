from django.db import models


# Create your models here.
class Employee(models.Model):
    """
    The Employee model with different fields.
    """
    name = models.CharField(max_length=20)
    eid = models.IntegerField()
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    company = models.CharField(max_length=20)
    department = models.CharField(max_length=20)

    class Meta:
        db_table = 'Employee'
