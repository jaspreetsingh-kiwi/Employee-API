from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    """
    Define the form class for the Employee model
    """
    name = forms.CharField(max_length=20)
    eid = forms.IntegerField()
    phone = forms.CharField(max_length=10)
    email = forms.CharField(max_length=20)
    address = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    state = forms.CharField(max_length=20)
    company = forms.CharField(max_length=20)
    department = forms.CharField(max_length=20)

    class Meta:
        """
           Use the Meta class to specify the model and fields that the ModelForm should work with
        """
        model = Employee
        fields = ['id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department']
