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

    """
    Use the Meta class to specify the model and fields that the serializer should work with
    """

    class Meta:
        model = Employee
        fields = ['id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department']

    def validate_eid(self, value):
        if value <= 0:
            raise serializers.ValidationError('Employee ID is not valid')
        return value

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    """
    Override the create method to add custom behavior when creating a new Employee instance
    """

    def create(self, validated_data):
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

    """
        Use the Meta class to specify the model and fields that the serializer should work with
    """

    class Meta:
        model = Employee
        fields = ['id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department']

    def validate_eid(self, value):
        if value <= 0:
            raise serializers.ValidationError('Employee is not valid')
        return value

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    """
    Override the update method to add custom behavior when updating an existing Employee instance
    """

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.eid = validated_data.get('eid', instance.eid)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.company = validated_data.get('company', instance.company)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        return instance
