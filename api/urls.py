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
    SchoolStudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    CategoryListView,
    ItemAPIView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ParentDeleteView,
)

urlpatterns = [

    path('school/login/', obtain_jwt_token, name='admin-login'),
    # path('school/register/parent/', UserCreateAPIView.as_view(), name='register-parent'),
    path('school/profile/', SchoolAPIView.as_view(), name='school-profile'),
    path('school/parent/account/', ParentCreateAPIView.as_view(), name='school-parent-account'),
    path('school/parent/<int:parent_id>/delete/', ParentDeleteView.as_view(), name='school-parent-delete'),
    # path('profile/parent/', ParentAPIView.as_view(), name='profile-parent'),

    path('list/parent/', ParentListAPIView.as_view(), name='list-parent'),

    path('school/students/list/', StudentListView.as_view(), name='students-list'),
    path('school/students/', SchoolStudentListView.as_view(), name='students-list'),
    path('school/student/<int:student_id>/detail/', StudentDetailView.as_view(), name='students-list'),
    path('school/student/<int:parent_id>/add/', StudentCreateView.as_view(), name='student-create'),
    
    path('school/student/<int:student_id>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('school/student/<int:student_id>/delete/', StudentDeleteView.as_view(), name='student-delete'),
  
    path('category/', CategoryListView.as_view(), name='category'),

    path('list/item/', ItemAPIView.as_view(), name='items'),
    path('create/item/', ItemCreateView.as_view(), name='create-item'),
    path('update/item/<int:item_id>', ItemUpdateView.as_view(), name='update-item'),
    path('delete/item/<int:item_id>', ItemDeleteView.as_view(), name='delete-item'),

 ]
