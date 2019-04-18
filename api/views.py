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
	UserCreateSerializer,
	UserUpdateSerializer,
	UserSerializer,
    # ParentListSerializer,
	# ParentDetailSerializer,
	# ParentCreateUpdateSerializer,
    SchoolStudentListSerializer,
	SchoolDetailSerializer,
	StudentCreateUpdateSerializer, 
	StudentListSerializer,
	ItemSerializer,
    SchoolItemListSerializer,
	ItemCreateUpdateSerializer,
	CategorySerializer,
)

from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from api.models import School, Parent, Student, Category, Item, Order, CartItem
from django.contrib.auth.models import User
from .permissions import IsSchoolAdmin, IsPrincipalDe

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


# class ParentAPIView(RetrieveAPIView):
# 	serializer_class = ParentDetailSerializer
# 	def get(self, request, format=None):
# 		profile = Profile.objects.get(parent=request.user)
# 		serializer = ProfileDetailSerializer(profile, context={'request': request})
# 		if request.user.is_anonymous:
# 			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
# 		return Response(serializer.data, status=HTTP_200_OK)


# class ParentCreateAPIView(CreateAPIView):
#     serializer_class = ParentCreateUpdateSerializer

#     def post(self, request, *args, **kwargs):
#         my_data = request.data
#         serializer = self.serializer_class(data=my_data)
#         if serializer.is_valid():
#             valid_data = serializer.data
#             new_data_user = {
#                 'username': valid_data['parent']['username'],
#             }
#             user_parent = User.objects.create(**new_data_user)
#             user_parent.set_password(valid_data['parent']['password'])
#             user_parent.save()
#             parent_new_data = {
#                 'parent' : User.objects.get(id=user_parent.id),
#             }
#             parent_obj = Parent.objects.create(**parent_new_data)
#             School_obj = School.objects.get(school_admin=request.user)
#             parent_obj.school.add(School_obj)
#             parent_obj.save()
#             return Response(valid_data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# class ParentListAPIView(APIView):
#     serializer_class = ParentListSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         school = School.objects.get(school_admin= request.user)
#         serializer = self.serializer_class(school, context={'request': request})
#         return Response(serializer.data, status=HTTP_200_OK)
    

# class ParentDeleteView(DestroyAPIView):
#     queryset = Parent.objects.all()
#     lookup_field = 'id'
#     lookup_url_kwarg = 'parent_id'
#     # permission_classes = [IsPrincipalDe]


class SchoolAPIView(APIView):
    serializer_class = SchoolDetailSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get(self, request, format=None):
        # try:
        school = School.objects.get(school_admin=request.user)
        serializer = self.serializer_class(school, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)
        # except:
        #     return Response({"message": "You are not the admin for this school"}, status=HTTP_400_BAD_REQUEST)


class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer


class SchoolStudentListView(APIView):
    serializer_class = SchoolStudentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        school = School.objects.get(school_admin= request.user)
        serializer = self.serializer_class(school, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

class StudentDetailView(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'
    # permission_classes = [IsAuthenticated, ]




# hear will change this list 
class StudentCreateView(CreateAPIView):
    serializer_class = StudentCreateUpdateSerializer
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
                parent_obj = Parent.objects.create(**{
                    'user' : user_obj
                })
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
    serializer_class = StudentCreateUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id' 
    # permission_classes = [IsAuthenticated, ]

class StudentDeleteView(DestroyAPIView):
    queryset = Student.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'
    # permission_classes = [IsAuthenticated, ]


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemAPIView(ListAPIView):
    # queryset = Item.objects.all()
    serializer_class = SchoolItemListSerializer

    def get(self, request, format=None):
        school = School.objects.get(school_admin= request.user)
        serializer = self.serializer_class(school, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)



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
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'

    
class ItemDeleteView(DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'item_id'
