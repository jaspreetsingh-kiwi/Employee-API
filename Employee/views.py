from django.shortcuts import render, redirect
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .forms import EmployeeForm
from .messages import CREATED_SUCCESSFULLY, BAD_REQUEST, DELETED_SUCCESSFULLY, UPDATED_SUCCESSFULLY, EMPLOYEE_API
from .models import Employee
from .serializers import EmployeeUpdateSerializer, EmployeeCreateSerializer

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, \
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly


# Create your views here.
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
            response = requests.post(EMPLOYEE_API, data=data)
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
    response = requests.get(EMPLOYEE_API)
    employees = response.json()
    return render(request, 'list_employee.html', {'employees': employees})


def retrieve_employee(request, pk):
    """
    Display the single instance of the Employee.
    """
    response = requests.get(f"{EMPLOYEE_API}{pk}/")
    employee = response.json()
    return render(request, 'retrieve_employee.html', {'employee': employee})


def update_employee(request, pk):
    """
    Update the selected instance of the Employee.
    """
    response = requests.get(f"{EMPLOYEE_API}{pk}/")
    data = response.json()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            """
            Use the form data to update the data through the API
            """
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
            response = requests.put(f"{EMPLOYEE_API}{pk}/", data=data)
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
    response = requests.delete(f"{EMPLOYEE_API}{pk}/")
    return redirect('list_employee')


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    The EmployeeViewSet class provides the CRUD (Create, Retrieve, Update, Delete) operations for the Employee model.
    """
    queryset = Employee
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['^name']
    # ordering_fields = ['id']

    def get_serializer_class(self):
        """
        The get_serializer_class method returns a ModelSerializer of Employee Model objects.
        """
        if self.action in ['list', 'create']:
            return EmployeeCreateSerializer
        return EmployeeUpdateSerializer

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of Employee Model objects.
        """
        return Employee.objects.filter().order_by('id')

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
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Creates a new instance of the Employee model.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            print(serializer.data)
            return Response({'message': CREATED_SUCCESSFULLY, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        serializer = self.get_serializer(emp, data=request.data)
        if serializer.is_valid():
            serializer.update(emp, serializer.validated_data)
            return Response({'message': UPDATED_SUCCESSFULLY, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Updates an existing instance of the Employee model, based on the primary key (pk).
        """
        emp = self.get_object()
        serializer = self.get_serializer(emp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(emp, serializer.validated_data)
            return Response({'message': UPDATED_SUCCESSFULLY, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a single instance of the Employee model, based on the primary key (pk).
        """
        self.get_object().delete()
        return Response({'message': DELETED_SUCCESSFULLY})
