from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import (
    UserCreateAPIView,
    UserUpdateAPIView,
    SchoolAPIView,
    ParentView,
    ParentStudentsView,
    ParentWalletView,
    SchoolStudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    StudentLimitView,
    CategoryListView,
    ItemAPIView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    CartItemCreateView,
    OrderCreateView,
    CheckoutView,
    RetrieveOrder,
    StudentXItemsView
)

urlpatterns = [

    path('school/login/', obtain_jwt_token, name='admin-login'),
    path('school/profile/', SchoolAPIView.as_view(), name='school-profile'),
    
    path('parent/profile/', ParentView.as_view(), name='parent-profile'),
    path('parent/students/', ParentStudentsView.as_view(), name='parent-students'),
    path('parent/wallet/',ParentWalletView.as_view(), name='parent-wallet'),
    path('parent/<int:student_id>/x_items/', StudentXItemsView.as_view(), name='student-Xitems'),
   
    path('school/students/', SchoolStudentListView.as_view(), name='students-list'),
    path('student/add/', StudentCreateView.as_view(), name='student-add'),
    path('student/<int:student_id>/detail/', StudentDetailView.as_view(), name='students-detail'),
    path('student/<int:student_id>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:student_id>/delete/', StudentDeleteView.as_view(), name='student-delete'),
    path('student/<int:student_id>/limit/', StudentLimitView.as_view(), name='student-limit'),
   
    
    path('category/', CategoryListView.as_view(), name='category'),

    path('list/item/', ItemAPIView.as_view(), name='items'),
    path('item/detail/<int:item_id>/', ItemDetailView.as_view(), name='item-detail'),
    path('create/item/', ItemCreateView.as_view(), name='create-item'),
    path('update/item/<int:item_id>/', ItemUpdateView.as_view(), name='update-item'),
    path('delete/item/<int:item_id>/', ItemDeleteView.as_view(), name='delete-item'),

    path('create/<int:student_id>/order/', OrderCreateView.as_view(), name='create-order'),
    path('cartItem/<int:Order_id>/create/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('checkout/<int:Order_id>/', CheckoutView.as_view(), name='checkout'),
    path('order/<int:order_id>/', RetrieveOrder.as_view(), name='retrieve-order')
 ]
