from rest_framework import serializers
from .models import Employee


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """
    Define the serializer class for the Employee model
    """
    name = serializers.CharField(max_length=20, required=True)
    eid = serializers.IntegerField(required=True)
    phone = serializers.CharField(max_length=10, required=True)
    email = serializers.CharField(max_length=20, required=True)
    address = serializers.CharField(max_length=20, required=True)
    city = serializers.CharField(max_length=20, required=True)
    state = serializers.CharField(max_length=20, required=True)
    company = serializers.CharField(max_length=20, required=True)
    department = serializers.CharField(max_length=20, required=True)

    class Meta:
        """
            Use the Meta class to specify the model and fields that the serializer should work with
        """
        model = Employee
        fields = ['id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department']

    def validate_eid(self, value):
        """
        Validate if employee id is less than 0.
        """
        if value <= 0:
            raise serializers.ValidationError('Employee is not valid')
        return value

    def validate_email(self, value):
        """
        Validate if employee email already exists.
        """
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        """
        Override the create method to add custom behavior when creating a new Employee instance
        """
        emp = Employee.objects.create(
            name=validated_data['name'],
            eid=validated_data['eid'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            address=validated_data['address'],
            city=validated_data['city'],
            state=validated_data['state'],
            company=validated_data['company'],
            department=validated_data['department'],

        )
        return emp


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """
       Define the serializer class for the Employee model
    """
    name = serializers.CharField(max_length=20, required=True)
    eid = serializers.IntegerField(required=True)
    phone = serializers.CharField(max_length=10, required=True)
    email = serializers.CharField(max_length=20, required=True)
    address = serializers.CharField(max_length=20, required=True)
    city = serializers.CharField(max_length=20, required=True)
    state = serializers.CharField(max_length=20, required=True)
    company = serializers.CharField(max_length=20, required=True)
    department = serializers.CharField(max_length=20, required=True)

    class Meta:
        """
        Use the Meta class to specify the model and fields that the serializer should work with
        """
        model = Employee
        fields = ['id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department']

    def validate_eid(self, value):
        """
        Validate if employee id is less than 0.
        """
        if value <= 0:
            raise serializers.ValidationError('Employee is not valid')
        return value

    def update(self, instance, validated_data):
        """
         Override the update method to add custom behavior when updating an existing Employee instance
        """
        emp = Employee.objects.filter(id=instance.id).update(
            name=validated_data['name'],
            eid=validated_data['eid'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            address=validated_data['address'],
            city=validated_data['city'],
            state=validated_data['state'],
            company=validated_data['company'],
            department=validated_data['department'],
        )
        # Retrieve updated instance from the database
        return emp
