from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

from .models import School, Parent, Student, Category, Item, Order, CartItem

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'password', 'email', 'token']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        new_user = User(username=username , first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        new_user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)

        validated_data["token"] = token
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name', 
            'email',           
        ]
class ParentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',         
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



class ParentCreateUpdateSerializer(serializers.ModelSerializer):
    parent = ParentCreateSerializer()
    class Meta:
        model = Parent
        fields = ['parent']


class ParentDetailSerializer(serializers.ModelSerializer):
    parent = UserSerializer()
    class Meta:
        model = Parent
        fields = ['parent', 'image', 'expense']

        
class SchoolDetailSerializer(serializers.ModelSerializer):
    principal = UserSerializer()
    parents = ParentDetailSerializer(many=True)
    class Meta:
        model = School
        fields = ['name', 'principal', 'parents']


class StudentListSerializer(serializers.ModelSerializer): 
    parent = UserSerializer()
    class Meta:
        model = Student
        fields = ['id','name', 'grade', 'parent', 'limit', 'health']

class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'grade', 'limit', 'health']
