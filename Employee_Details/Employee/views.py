from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
import requests
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .forms import EmployeeForm
from .models import Employee
from .serializers import EmployeeUpdateSerializer, EmployeeCreateSerializer


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
    response = requests.get(f"http://127.0.0.1:8000/employee/{pk}/")
    data = response.json()
    print(data)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Use the form data to update the data through the API
            data = {'name': form.cleaned_data['name'],
                    'eid': form.cleaned_data['eid'],
                    'phone': form.cleaned_data['phone'],
                    'email': form.cleaned_data['email'],
                    'address': form.cleaned_data['address'],
                    'city': form.cleaned_data['city'],
                    'state': form.cleaned_data['state'],
                    'company': form.cleaned_data['company'],
                    'department': form.cleaned_data['department'],
                    }
            print(data)
            response = requests.put(f'http://127.0.0.1:8000/employee/{pk}/', data=data)
            if response.status_code == 201:
                return redirect('list_employee')
            else:
                return render(request, 'update_employee.html')
    else:
        form = EmployeeForm(initial=data)
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
    queryset = Employee

    def get_serializer_class(self):
        if self.action == ['list', 'create']:
            return EmployeeCreateSerializer
        else:
            return EmployeeUpdateSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Employee Model objects.
        """
        return Employee.objects.all()

    def list(self, request, *args, **kwargs):
        """
         Returns a list of all instances of the Employee model.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single instance of the Employee model, based on the primary key (pk).
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the Employee model.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        serializer = self.get_serializer(emp, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Updates an existing instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        serializer = self.get_serializer(emp, data=request.data, partial=True)
        if serializer.is_valid():
            self.partial_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        emp.delete()
        return Response({'msg': 'Data Deleted'})
