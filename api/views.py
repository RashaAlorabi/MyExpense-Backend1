from django.shortcuts import redirect

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
   
)

from .serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserSerializer,
    ParentDetailSerializer,
    ParentCreateUpdateSerializer,
    SchoolDetailSerializer,
    StudentCreateUpdateSerializer, 
    StudentListSerializer
)

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from api.models import School, Parent, Student, Category, Item, Order, CartItem
from django.contrib.auth.models import User
from .permissions import IsPrincipal

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


class ParentCreateAPIView(CreateAPIView):
    serializer_class = ParentCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        my_data = request.data
        serializer = self.serializer_class(data=my_data)
        if serializer.is_valid():
            valid_data = serializer.data
            print("valid_data ===> ", valid_data)
            print("valid_data_parent ===> ", valid_data['parent']['username'])
            new_data_user = {
                'username': valid_data['parent']['username'],
            }
            user_parent = User.objects.create(**new_data_user)
            user_parent.set_password(valid_data['parent']['password'])
            user_parent.save()
            parent_new_data = {
                'parent' : User.objects.get(id=user_parent.id),
                'school': School.objects.get(principal=request.user),
            }
            parent_obj = Parent.objects.create(**parent_new_data)
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ParentListAPIView(ListAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentDetailSerializer


class SchoolAPIView(APIView):
    serializer_class = SchoolDetailSerializer
    permission_classes = [IsAuthenticated, IsPrincipal]

    def get(self, request, format=None):
        try:
            school = School.objects.get(principal=request.user)
            serializer = self.serializer_class(school, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response({"message": "You are not a principle"}, status=HTTP_400_BAD_REQUEST)


class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

class StudentCreateView(CreateAPIView):
    serializer_class = StudentCreateUpdateSerializer
    # permission_classes = [IsAuthenticated, ]
    

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

        
