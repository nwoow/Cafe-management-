from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Room)
admin.site.register(Category)
# admin.site.register(SubCategory)
admin.site.register(Food)
admin.site.register(OrderPlaced)
admin.site.register(BookingFood)