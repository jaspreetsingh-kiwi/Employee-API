from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Define the serializer class for the Employee model
    """
    name = serializers.CharField(max_length=20)
    eid = serializers.IntegerField()
    phone = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=20)
    state = serializers.CharField(max_length=20)
    company = serializers.CharField(max_length=20)
    department = serializers.CharField(max_length=20)

    """
    Use the Meta class to specify the model and fields that the serializer should work with
    """
    class Meta:
        model = Employee
        fields = ['id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department']

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
        # instance.perform_update()
        return instance
