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
	ParentListSerializer,
	ParentCreateUpdateSerializer,
	SchoolDetailSerializer,
	StudentCreateUpdateSerializer, 
	StudentListSerializer,
	ItemSerializer,
	ItemCreateUpdateSerializer,
	CategorySerializer,

)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from api.models import School, Parent, Student, Category, Item, Order, CartItem
from django.contrib.auth.models import User





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


class ParentAPIView(RetrieveAPIView):
	serializer_class = ParentDetailSerializer

	def get(self, request, format=None):
		profile = Profile.objects.get(user=request.user)
		serializer = ProfileDetailSerializer(profile, context={'request': request})
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		return Response(serializer.data, status=HTTP_200_OK)


class ParentCreateAPIView(CreateAPIView):
	serializer_class = ParentCreateUpdateSerializer

	def perform_create(self, serializer):
		school_obj = School.objects.get(principal= self.request.user)
		serializer.save(school = school_obj)

class ParentListAPIView(ListAPIView):
	queryset = Parent.objects.all()
	serializer_class = ParentListSerializer


class SchoolAPIView(RetrieveAPIView):
	serializer_class = SchoolDetailSerializer

	def get(self, request, format=None):
		school = School.objects.get(principal=request.user)
		serializer = SchoolDetailSerializer(school, context={'request': request})
		if request.user.is_anonymous:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		return Response(serilazers.data, status=HTTP_200_OK)


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


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemAPIView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemCreateView(CreateAPIView):
    serializer_class = ItemCreateUpdateSerializer

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