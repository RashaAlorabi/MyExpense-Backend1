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
# class ParentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'id',
#             'username',
#             'password',         
#         ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# class ParentCreateUpdateSerializer(serializers.ModelSerializer):
#     parent = ParentCreateSerializer()
#     class Meta:
#         model = Parent
#         fields = ['parent']


class StudentParentSerializer1(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Parent
        fields = ['user', 'image', 'wallet'] 


class StudentListSerializer(serializers.ModelSerializer): 
    parent=StudentParentSerializer1()
    class Meta:
        model = Student
        fields = ['id','name', 'grade', 'limit', 'health','parent','image']


# class ParentDetailSerializer(serializers.ModelSerializer):
#     parent = UserSerializer()
#     # child = StudentListSerializer(many=True)
#     class Meta:
#         model = Parent
#         fields = ['id','parent','image', 'wallet']

# class ParentListSerializer(serializers.ModelSerializer):
#     # parents = ParentDetailSerializer(many=True)
#     class Meta:
#         model = School
#         fields = ['parents']
        
# class ParentCreateSer(serializers.ModelSerializer):
#     class Meta:
#         model = Parent
#         fields = ['NationalـId']
        
class StudentCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(min_value=1, max_value=999999999)
    email = serializers.EmailField()
    class Meta:
        model = Student
        fields = ['parent_id', 'email', 'name', 'grade', 'limit', 'health','image']

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'grade', 'limit', 'health','image']

class SchoolStudentListSerializer(serializers.ModelSerializer):
    students = StudentListSerializer(many=True)
    class Meta:
        model = School
        fields = ['students']


        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category= CategorySerializer()
    class Meta:
        model = Item
        fields = [
            'id',
			'name',
			'price',
			'description',
			'stock',
            'image',
			'category',
            'school',
        ]


class SchoolItemListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = School
        fields = ['items']

class SchoolDetailSerializer(serializers.ModelSerializer):
    school_admin = UserSerializer()
    items = ItemSerializer(many=True)
    students = StudentListSerializer(many=True)
    class Meta:
        model = School
        fields = ['name', 'school_admin', 'students', 'items']

class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'stock', 'image', 'category',]

class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id',
            'item',
            'quantity',
        ]