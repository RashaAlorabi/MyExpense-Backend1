from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from .models import School, Parent, Student, Category, Item, Order, CartItem

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


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class StudentParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Parent
        fields = ['user', 'image', 'wallet'] 


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


class ParentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['not_alloweds']


class StudentListSerializer(serializers.ModelSerializer): 
    parent=StudentParentSerializer()
    not_allowed = ItemSerializer(many=True)
    
    class Meta:
        model = Student
        fields = ['id','name','grade', 'limit', 'health','parent','image','not_allowed']


class SchoolDetailSerializer(serializers.ModelSerializer):
    school_admin = UserSerializer()
    items = ItemSerializer(many=True)
    students = StudentListSerializer(many=True)
    class Meta:
        model = School
        fields = ['name', 'school_admin', 'students', 'items']

# remove
class UpdateWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['wallet']


class UpdatelimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['limit']


class StudentCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(min_value=1, max_value=9999999999)
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


class SchoolCategoriesSerializer(serializers.ModelSerializer):
    schoolcategories = CategorySerializer(many=True)
    class Meta:
        model = School
        fields = ['schoolcategories']


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'stock', 'image', 'category',]


class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    # item = ItemSerializer()
    class Meta:
        model = CartItem
        fields = [
            'id',
            'item',
            'quantity',
        ]
class CartItemListSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = CartItem
        fields = [
            'id',
            'item',
            'quantity',
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['student']


class RetrieveOrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemListSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','total', 'paid', 'order_date', 'cart_items']

    
class StudentDetailSerializer(serializers.ModelSerializer):
    orders= RetrieveOrderSerializer(many=True)
    school = SchoolItemListSerializer()
    class Meta:
        model = Student
        fields = ['id','name', 'grade', 'school', 'limit', 'health','image', 'orders']

class ParentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    child = StudentDetailSerializer(many=True)
    class Meta:
        model = Parent
        fields = ['user', 'child', 'wallet', 'image']

