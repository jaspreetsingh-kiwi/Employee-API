from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
import requests
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .forms import EmployeeForm
from .models import Employee
from .serializers import EmployeeSerializer


def create_employee(request):
    """
    Create an instance of the Employee.
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Retrieve the cleaned form data
            data = form.cleaned_data
            # Send a POST request to the API to add a new employee
            url = 'http://127.0.0.1:8000/employee/'
            response = requests.post(url, data=data)
            # Check if the API response was successful
            if response.status_code == 201:
                employee = response.json()
                return redirect('list_employee')
    else:
        form = EmployeeForm()
    return render(request, 'create_employee.html', {'form': form})


def list_employee(request):
    """
       Display the instances of the Employee.
    """
    # Send a GET request to the API to retrieve the employee data
    response = requests.get("http://127.0.0.1:8000/employee/")
    employees = response.json()
    return render(request, 'list_employee.html', {'employees': employees})


def retrieve_employee(request, pk):
    """
          Display the single instance of the Employee.
    """
    response = requests.get(f"http://127.0.0.1:8000/employee/{pk}/")
    employee = response.json()
    return render(request, 'retrieve_employee.html', {'employee': employee})


def update_employee(request, pk):
    """
       Update or partially update an Employee instance.
    """
    # Send a GET request to the API to retrieve the employee data
    url = f'http://127.0.0.1:8000/employee/{pk}/'
    response = requests.get(url)
    # Check if the API response was successful
    if response.status_code == 200:
        # Deserialize the API response and store it in the employee dictionary
        employee = response.json()
        # Initialize the form with the employee data
        form = EmployeeForm(initial=employee)
    else:
        form = EmployeeForm()

    if request.method == 'POST':
        # Update the form with the data from the request
        form = EmployeeForm(request.POST)
        # Check if the form data is valid
        if form.is_valid():
            # Prepare the updated employee data
            employee = form.cleaned_data
            # Send a PUT or PATCH request to the API to update or partially update the employee instance
            if request.PUT:
                response = requests.put(url, data=employee)
            elif request.PATCH:
                response = requests.patch(url, data=employee)
            # Check if the API response was successful
            if response.status_code in [200, 201]:
                return redirect('show_employee')

    return render(request, 'update_employee.html', {'form': form})


def delete_employee(request, pk):
    """
       Delete the selected Employee instance.
    """
    # Send a DELETE request to the API to delete the employee
    url = f'http://127.0.0.1:8000/employee/{pk}/'
    response = requests.delete(url)

    # Redirect the user back to the list of employees after to delete
    return redirect('list_employee')


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    The EmployeeViewSet class provides the CRUD (Create, Retrieve, Update, Delete) operations for the Employee model.
    """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Employee Model objects.
        """
        return Employee.objects.all()

    def list(self, request, *args, **kwargs):
        """
         Returns a list of all instances of the Employee model.
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single instance of the Employee model, based on the primary key (pk).
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the Employee model.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        serializer = self.serializer_class(emp, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Updates an existing instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        serializer = self.serializer_class(emp, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        emp.delete()
        return Response({'msg': 'Data Deleted'})
