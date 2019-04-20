from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator



        
class School(models.Model):
    name = models.CharField(max_length=50)
    school_admin = models.OneToOneField(User, on_delete=models.CASCADE,)
    
    def __str__ (self):
        return self.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='parent_image', null=True, blank=True)
    wallet = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    # NationalـId = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(1), MaxValueValidator(9999999999)], null=False, blank=False)
    def __str__(self):
        return self.user.username

Garad=[('Grade 1','Grade 1'),
         ('Grade 2','Grade 2'),
         ('Grade 3','Grade 3'),
         ('Grade 4','Grade 4'),
         ('Grade 5','Grade 5'),
         ('Grade 6','Grade 6'),
        ]
class Student(models.Model):
    name = models.CharField(max_length=50)
    grade = models.CharField(choices=Garad, default=1, max_length=10)
    parent = models.ForeignKey(Parent, on_delete = models.CASCADE, related_name='child')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    limit = models.PositiveIntegerField(validators=[MinValueValidator(1)] , default=1)
    image = models.ImageField(upload_to='student_image', null=True, blank=True)
    health = models.CharField(max_length=50)

    def __str__(self):
        return self.name	

        
class Category(models.Model):
    name = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="schoolcategories")

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)] , default=0)
    image = models.ImageField(upload_to='item_image', null=True, blank=True)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="items")
    
    def __str__(self):
        return self.name


class Order(models.Model):
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False) 
    order_date = models.DateTimeField(null=True)

    def get_total(self):
        total = 0
        if self.cart_items.all():
            for item in self.cart_items.all():
                total += item.subtotal
        return total


class CartItem(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    subtotal = models.DecimalField(default=0.00,max_digits=10, null=True, decimal_places=2)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='cart_items')

 
  
@receiver(pre_save, sender = CartItem)
def get_subtotal(instance, *args, **kwargs):
    instance.subtotal = Decimal(instance.item.price)*Decimal(instance.quantity)
    instance.item.save()

@receiver(pre_delete, sender = CartItem)
def change_stock(instance, *args, **kwargs):
    instance.item.stock = int(instance.item.stock) + int(instance.quantity)
    instance.item.save()
