from django.contrib import admin

from django.contrib import admin
from .models import Item, Category, School, Parent, Student, Order, CartItem


admin.site.register(School)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Item)
admin.site.register(Category)

