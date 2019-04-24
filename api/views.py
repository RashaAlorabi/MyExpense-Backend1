from django.shortcuts import redirect
from rest_framework.parsers import FileUploadParser
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)

from django.utils.crypto import get_random_string

from .serializers import (
    StudentDetailSerializer,
	UserCreateSerializer,
	UserUpdateSerializer,
	UserSerializer,
    CartItemCreateUpdateSerializer,
    SchoolStudentListSerializer,
	SchoolDetailSerializer,
    ParentDetailSerializer,
	StudentCreateSerializer, 
    StudentUpdateSerializer, 
	StudentListSerializer,
    UpdatelimitSerializer,
	ItemSerializer,
    SchoolItemListSerializer,
    ItemCreateUpdateSerializer,
    CategorySerializer,
    SchoolCategoriesSerializer,
    StudentParentSerializer1,
    UpdateWalletSerializer,
    OrderSerializer,
    RetrieveOrderSerializer,

)

from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from api.models import School, Parent, Student, Category, Item, Order, CartItem
from django.contrib.auth.models import User
from .permissions import IsSchoolAdmin, IsParent

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(RetrieveUpdateAPIView):
    
    def put(self, request, format=None):
        user= request.user
        serializer = UserUpdateSerializer(user, data=request.data, )
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user,context={'request': request}).data, status=HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SchoolAPIView(APIView):
    serializer_class = SchoolDetailSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get(self, request, format=None):
        try:
            school = School.objects.get(school_admin=request.user)
            serializer = self.serializer_class(school, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response({"message": "You are not the admin for this school"}, status=HTTP_400_BAD_REQUEST)

class ParentView(APIView):
    serializer_class = ParentDetailSerializer
    permission_classes = [IsParent]

    def get(self, request, format=None):
        try:
            parent = Parent.objects.get(user=request.user)
            serializer = self.serializer_class(parent, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response({"message": "you are not a parent "}, status=HTTP_400_BAD_REQUEST)

class ParentStudentsView(ListAPIView):
    serializer_class = StudentDetailSerializer
    permission_classes = [IsParent]
    
    def get_queryset(self):
        return self.request.user.parent.child.all()

class ParentWalletView(RetrieveUpdateAPIView):
    serializer_class = UpdateWalletSerializer
    permission_classes = [IsParent]
    
    def put(self, request, *args, **kwargs):
        parent_id = kwargs
        my_data = request.data
       
        serializer = self.serializer_class(data=my_data, )
        if serializer.is_valid():

            parent_obj = Parent.objects.get(user= request.user)
            valid_data = serializer.data
            print("valid_data ==> ", valid_data)
            parent_obj.wallet = valid_data['wallet']
            parent_obj.save()
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class StudentLimitView(RetrieveUpdateAPIView):
    serializer_class = UpdatelimitSerializer
    permission_classes = [IsParent]
    
    def put(self, request, *args, **kwargs):
        student_id = kwargs
        my_data = request.data
       
        serializer = self.serializer_class(data=my_data, )
        if serializer.is_valid():
            student_obj = Student.objects.get(id= student_id["student_id"])
            parent_obj = Parent.objects.get(user= request.user)
            valid_data = serializer.data
            student_obj.limit = valid_data['limit']
            student_obj.save()
            parent_obj.save()
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SchoolStudentListView(ListAPIView):
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.school.students.all()

class StudentDetailView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'
    permission_classes = [IsAuthenticated, ]




# hear will change this list 
class StudentCreateView(APIView):
    serializer_class = StudentCreateSerializer
    # permission_classes = [IsAuthenticated, ]
    
    def post(self, request, *args, **kwargs):
        my_data = request.data
        print("my_data ==> ", my_data)
        serializer = self.serializer_class(data=my_data)
        if serializer.is_valid():
            print("serializer ==> ", serializer)
            valid_data = serializer.data
            print("valid_data ==>  ", valid_data)
            user_obj , created = User.objects.get_or_create(username = "par"+str(valid_data['parent_id']), email=valid_data['email'])
            if created:
                password = get_random_string()
                user_obj.set_password(password)
                user_obj.save()
                parent_obj = Parent.objects.create(**{'user':user_obj})
                subject = "معلومات الدخول إلى نظام مصروفي"
                message = " "+password+" كلمة المرور \n "+user_obj.username+" اسم المستخدم"

                """ Name of user """
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_obj.email]
                send_mail( subject, message, email_from, recipient_list )
            else:
                parent_obj = Parent.objects.get(user=user_obj)

            new_student = {
                 'parent': parent_obj,
                 'name': valid_data['name'],
                 'grade': valid_data['grade'],
                 'health': valid_data['health'],
                 'image' :  my_data['image'],
                 'school': School.objects.get(school_admin=request.user),
                }
            student = Student.objects.create(**new_student)
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




class StudentUpdateView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id' 
    permission_classes = [IsAuthenticated, ]

class StudentDeleteView(DestroyAPIView):
    queryset = Student.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'
    permission_classes = [IsAuthenticated, ]


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.request.user.school.schoolcategories.all()
    

class ItemAPIView(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.request.user.school.items.all()


class ItemDetailView(RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'
    # permission_classes = [IsAuthenticated, ]


class ItemCreateView(CreateAPIView):
    serializer_class = ItemCreateUpdateSerializer
    # permission_classes = [IsAuthenticated, ]
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
        my_data = request.data
        print("my_data ==> ", my_data)
        serializer = self.serializer_class(data=my_data, )
        if serializer.is_valid():
            print("serializer ==> ", serializer)
            valid_data = serializer.data
            print("valid_data ==>  ", valid_data)
            school_obj = School.objects.get(school_admin= request.user)
            new_item = {
                'name': valid_data['name'],
                'price': valid_data['price'],
                'description': valid_data['description'],
                'stock': valid_data['stock'],
                'image': my_data['image'],
                'category': Category.objects.get(id=valid_data['category']),
                'school': school_obj,
            }
            item = Item.objects.create(**new_item)
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ItemUpdateView(RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemCreateUpdateSerializer
    

    def put(self, request, *args, **kwargs):
        item_id = kwargs
        my_data = request.data
       
        serializer = self.serializer_class(data=my_data, )
        if serializer.is_valid():

            Item_obj = Item.objects.get(id= item_id["item_id"])
            valid_data = serializer.data
            school_obj = School.objects.get(school_admin= request.user)
            
            Item_obj.name = valid_data['name']
            Item_obj.price = valid_data['price']
            Item_obj.description = valid_data['description']
            Item_obj.stock = valid_data['stock']
            Item_obj.image = my_data['image']
            Item_obj.category = Category.objects.get(id=valid_data['category'])
            Item_obj.school = school_obj

            Item_obj.save()
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class ItemDeleteView(DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'


class CartItemCreateView(CreateAPIView):
    serializer_class = CartItemCreateUpdateSerializer
    
    def post(self, request, *args, **kwargs):
        my_data = request.data
        id_order = kwargs
        serializer = self.serializer_class(data=my_data)
        if serializer.is_valid():
            valid_data = serializer.data
            new_data = {
                'item': Item.objects.get(id=valid_data['item']),
                'order': Order.objects.get(id=id_order['Order_id']),
            }
            cartItem, created = CartItem.objects.get_or_create(**new_data)
            if created:
                cartItem.quantity = valid_data['quantity']
                cartItem.save()
                cartItem.item.stock -= cartItem.quantity
                cartItem.item.save()
                return Response(valid_data, status=HTTP_200_OK)
            else:
                cartItem.item.stock +=  cartItem.quantity
                cartItem.quantity += valid_data['quantity']
                cartItem.save()
                cartItem.item.stock -= cartItem.quantity
                cartItem.item.save()
                return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(student=Student.objects.get(id=self.kwargs['student_id']))

class CheckoutView(APIView):

    def post(self, request, *args, **kwargs):
        order= Order.objects.get(id=self.kwargs['Order_id'])
        order.paid = True
        order.save()
        return order

class RetrieveOrder(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = RetrieveOrderSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'order_id'

            
