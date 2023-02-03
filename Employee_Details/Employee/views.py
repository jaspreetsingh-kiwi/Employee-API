from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from .forms import EmployeeForm
from .models import Employee
from .serializers import EmployeeSerializer


def Details(request):
    form = EmployeeForm
    return render(request, 'Home.html', {'form': form})


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    The EmployeeViewSet class provides the CRUD (Create, Retrieve, Update, Delete) operations for the Employee model.
    """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get_queryset(self):
        """
        The get_queryset method returns a queryset of YourModel objects.
        """
        return Employee.objects.all()

    def list(self, request, *args, **kwargs):
        """
         Returns a list of all instances of the Employee model.
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single instance of the Employee model, based on the primary key (pk).
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

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
