from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.core.mail import send_mail


        
class School(models.Model):
    name = models.CharField(max_length=50)
    school_admin = models.OneToOneField(User, on_delete=models.CASCADE,)
    
    def __str__ (self):
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

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='parent_image', null=True, blank=True)
    wallet = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    # NationalـId = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(1), MaxValueValidator(9999999999)], null=False, blank=False)
    def __str__(self):
        return self.user.username

Garad=[('الصف الاول','الصف الاول'),
         ('الصف الثاني','الصف الثاني'),
         ('الصف الثالث','الصف الثالث'),
         ('الصف الرابع','الصف الرابع'),
         ('الصف الخامس','الصف الخامس'),
         ('الصف السادس','الصف السادس'),
        ]

class Student(models.Model):
    name = models.CharField(max_length=50)
    grade = models.CharField(choices=Garad, default=1, max_length=20)
    parent = models.ForeignKey(Parent, on_delete = models.CASCADE, related_name='child')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    limit = models.PositiveIntegerField(validators=[MinValueValidator(1)] , default=1)
    image = models.ImageField(upload_to='student_image', null=True, blank=True)
    health = models.CharField(max_length=50)
    not_allowed = models.ManyToManyField(Item, related_name="not_alloweds",  blank=True)
    def __str__(self):
        return self.name	

    
class Order(models.Model):
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False) 
    order_date = models.DateTimeField(auto_now_add=True)

    def sum_total(self):
        all_item = self.cart_items.all()
        self.total = sum([item_obj.quantity * item_obj.item.price for item_obj in all_item])
        self.save()

    def checkout(self):
        if self.paid:
            self.student.parent.wallet -= self.total
            self.student.parent.save()
        if self.student.parent.wallet <=10:
            subject = "رصيد المحفظة اوشك علي الانتهاء"
            message =  ("السلام عليكم نود ان نبلغكم ان المبلغ المتبقي في المحفظة الخاصة بكم هو %d  نرجو منكم اعادة شحنها في اقرب وقت ممكن ") %(self.student.parent.wallet)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.student.parent.user.email]
            print(recipient_list,"recipient_list")
            send_mail( subject, message, email_from, recipient_list )
   
    def __str__(self):
        return ("%s T %s") % (self.student.name ,self.order_date)


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=0)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='cart_items')

    def __str__(self):
        return ("%s q %s") % (self.item.name , self.quantity)

 
  
@receiver(post_delete, sender=CartItem)
@receiver(post_save, sender=CartItem)
def get_total(instance, *args, **kwargs):
    instance.order.sum_total()

@receiver(post_save, sender=Order)
def checkout(instance, *args, **kwargs):
    instance.checkout()
