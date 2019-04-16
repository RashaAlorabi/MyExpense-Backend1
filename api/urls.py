from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import (
    UserCreateAPIView,
    UserUpdateAPIView,
    # ParentAPIView,
    ParentListAPIView,
    ParentCreateAPIView,
    SchoolAPIView,
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    
)

urlpatterns = [

    path('login/', obtain_jwt_token, name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register-parent'),
    path('profile/school/', SchoolAPIView.as_view(), name='profile-school'),
    path('parent/create/school/', ParentCreateAPIView.as_view(), name='parent-create-school'),
    # path('profile/parent/', ParentAPIView.as_view(), name='profile-parent'),
    path('list/parent/', ParentListAPIView.as_view(), name='list-parent'),

    path('students/', StudentListView.as_view(), name='students-list'),
    path('student/add/', StudentCreateView.as_view(), name='student-create'),
    path('student/<int:student_id>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:student_id>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]
