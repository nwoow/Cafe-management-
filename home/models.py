import qrcode
from distutils.command.upload import upload
from django.db import models
from io import BytesIO
from django.core.files import File
from PIL import Image 
import os
import uuid
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class CategoryManager(models.Manager):
    def with_food_tag(self, tag):
        print(tag)
        return self.filter(food__tags=tag).distinct()

class Category(models.Model):
    title = models.CharField(max_length=180)
    image = models.ImageField(upload_to='category',null=True,blank=True)

    objects = CategoryManager()

    def __str__(self):
        return self.title


# class SubCategory(models.Model):
#     category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='category')
#     title = models.CharField(max_length=180)
#     image = models.ImageField(upload_to='category',null=True,blank=True)

#     def __str__(self):
#         return self.title

TAG_CHOICES = (
    ('Veg','Veg'),
    ('Non Veg','Non Veg'),
)


class Food(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='food')
    title = models.CharField(max_length=180)
    image = models.ImageField(upload_to='category',null=True,blank=True)
    price = models.IntegerField()
    desc = models.TextField()
    tags = models.CharField(max_length=50,choices=TAG_CHOICES)

    def __str__(self):
        return self.title


class Room(models.Model):
    block = models.CharField(max_length=120)
    room_no = models.CharField(max_length=120)
    qr_code = models.FileField(upload_to='qrcode',blank=True,null=True)


    def __str__(self):
        return self.room_no


    def save(self,*args,**kwargs):
        qr_image = qrcode.make(
            'http://127.0.0.1:8000/menu/?block='+self.block +'&roomno='+self.room_no
        )
        qr_offset = Image.new('RGB',(405,405),'white')
        qr_offset.paste(qr_image)
        files_name = f'(self.sl_no)qr.png'
        buffer = BytesIO()
        qr_offset.save(buffer,'PNG')
        self.qr_code.save(files_name,File(buffer),save=False)
        qr_offset.close()
        return super().save(*args, **kwargs)



STATUS_CHOICES = (
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Canceled','Canceled')
)

class OrderPlaced(models.Model):
    invoice_no = models.CharField(max_length=40)
    device_id = models.CharField(max_length=180)
    block = models.CharField(max_length=120)
    room_no = models.CharField(max_length=120)
    ordered_date = models.DateTimeField(auto_now_add=True)
    merchantTransactionId = models.CharField(max_length=200)
    transactionId = models.CharField(max_length=200)
    paid_amount = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = self.generate_invoice_no()
        super().save(*args, **kwargs)

    def generate_invoice_no(self):
        # Generate a unique invoice number
        date_str = now().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:6].upper()
        return f'CA{date_str}{unique_id}'

    @property
    def total_price(self):
        totalprice =[]
        for f in self.booking_food_det.all():
            totalprice.append(f.food.price*f.quantity)
        return sum(totalprice)


class BookingFood(models.Model):
    booking = models.ForeignKey(OrderPlaced,on_delete=models.CASCADE,related_name="booking_food_det")
    food = models.ForeignKey(Food,on_delete=models.SET_NULL,null=True,blank=True,related_name="booking_Food")
    quantity = models.PositiveIntegerField(default=1)

class FoodReview(models.Model):
    food = models.ForeignKey(Food, on_delete=models.SET_NULL,null=True,blank=True,related_name="food_reviews")
    rating = models.SmallIntegerField( default=0,validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

