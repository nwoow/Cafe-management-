from django.shortcuts import render,redirect
# from num2words import num2words
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from . models import *
import uuid
from django.db import transaction
# Create your views here.


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None and user.is_staff == True:
            login(request,user)
            messages.success(request, 'You are Logged in')
            return redirect('dashboard')     
        else:
            messages.error(request,'Your Username or Password is incorrect')
            return redirect('/')
    return render(request,'index.html')


def dashboard(request):
    return render(request,'dashboard.html')


def generateqr(request):
    if request.method == "POST":
        block = request.POST['block']
        room_no = request.POST['room_no']
        room = Room(block=block,room_no=room_no)
        room.save()
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request,'generateqr.html',context)


def viewqr(request,id):
    room = Room.objects.get(id=id)
    context = {'room':room}
    return render(request,'viewqr.html',context)


def delqr(request,id):
    room = Room.objects.get(id=id)
    room.delete()
    return redirect('generateqr')


def addcategory(request):
    if request.method =="POST":
        title = request.POST['title']
        image = request.FILES['image']
        if Category.objects.filter(title=title):
            print('category already exists')
        else:
            category = Category(title=title,image=image)
            category.save()
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'addcategory.html',context)

def delcategory(request,id): 
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('addcategory')

# def addsubcategory(request):
#     if request.method =="POST":
#         title = request.POST['title']
#         image = request.FILES['image']
#         category = request.POST['category']
#         if SubCategory.objects.filter(title=title).exists():
#             pass
#         else:
#             subcategory = SubCategory(
#                 title=title,image=image,
#                 category=Category.objects.get(id =category)   
#             )
#             subcategory.save()

#     category = Category.objects.all()
#     subcategory =SubCategory.objects.all()
#     context = {'category':category,'subcategory':subcategory}
#     return render(request,'addsubcategory.html',context)


# def delsubcategory(request,id):
#     subcategory = SubCategory.objects.get(id=id)
#     subcategory.delete()
#     return redirect('addsubcategory')


def addmenu(request):
    if request.method =="POST":
        title = request.POST['title']
        image = request.FILES['image']
        category = request.POST['category']
        tags = request.POST['tags']
        price = request.POST['price']
        desc = request.POST['desc']
        food = Food(
            title=title,image=image,
            category=Category.objects.get(id =category),
            price=price,desc=desc,
            tags=tags
        )
        food.save()
    menu = Food.objects.all()
    category =Category.objects.all()
    context = {'menu':menu,'category':category}
    return render(request,'addmenu.html',context)


def delmenu(request,id):
    menu = Food.objects.get(id=id)
    menu.delete()
    return redirect('addmenu')


def viewmenu(request):
    if 'device_id' not in request.session:
        request.session['device_id'] = str(uuid.uuid4())  
    block = request.GET.get('block')
    room_no = request.GET.get('roomno')
    cat = request.GET.get('cat')
    request.session['block'] = block
    request.session['room_no'] = room_no
    block = request.session.get('block')
    room_no = request.session.get('room_no')
    if cat:
        category =Category.objects.with_food_tag(cat)
        print(category)
    else:
        category = Category.objects.all()
    context = {'rblock':block,'room_no':room_no,'category':category}
    return render(request,'viewmenu.html',context)


def viewmenuview(request):
    block = request.session.get('block')
    room_no = request.session.get('room_no')
    cat = request.GET.get('cat')
    category = Category.objects.all()
    food = Food.objects.filter(category__title=cat)
    context = {'rblock':block,'room_no':room_no,'food':food,'category':category}
    return render(request,'viewmenuview.html',context)


def add_to_cart(request):
    if request.method == "POST":
        id = request.POST['id']
        quantity = request.POST['quantity']
        food = Food.objects.get(id=id)
        cart = request.session.get('cart') 
        print(cart) 
        if cart:
            desc = cart.get(id)
            if desc:
                print('food in cart')
                cart[id] = quantity
            else:
                print('food not in cart')
                cart[id] = quantity
        else:
            cart ={}  
            cart[id]=quantity
        request.session['cart']=cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    block = request.session.get('block')
    room_no = request.session.get('room_no')
    context = {'rblock':block,'room_no':room_no}
    return render(request,'cart.html',context)


def delcart(request,id):
    cart = request.session['cart']
    del cart[str(id)]
    request.session["cart"] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def placeorder(request):
    if 'device_id' not in request.session:
        request.session['device_id'] = str(uuid.uuid4())
    device_id = request.session.get('device_id')
    cart = request.session.get('cart', {})
    block = request.session.get('block')
    room_no = request.session.get('room_no')
    if not cart:
        return render(request, 'order.html', {'message': 'Your cart is empty.'})
    try:
        with transaction.atomic():
            orderplaced = OrderPlaced.objects.create(device_id=device_id,block=block,room_no=room_no)
            for food_id, quantity in cart.items():
                food = Food.objects.filter(id=food_id).first()
                if food:
                    booking = BookingFood(
                        booking=orderplaced,
                        food=food,
                        quantity=quantity
                    )
                    booking.save()

            # Clear the cart after placing the order
            request.session['cart'] = {}

    except Exception as e:
        # Log the exception and show an error message
        # log_error(e)  # Assuming you have a logging function
        return render(request, 'order.html', {'message': 'There was an error placing your order. Please try again.'})
    return redirect('vieworderdet')
    # return render(request, 'order.html', {'message': 'Order placed successfully!'})


def vieworderdet(request):
    if 'device_id' not in request.session:
        pass
    device_id = request.session.get('device_id')
    print(device_id)
    order = OrderPlaced.objects.filter(device_id = device_id)
    print(order)
    context = {'order':order}
    return render(request,'order.html',context)


# manage oreder by admin pannel

def pending(request):
    order = OrderPlaced.objects.filter(status= "Pending")
    context = {'order':order}
    return render(request,'order/pending.html',context)


def accepted(request):
    order = OrderPlaced.objects.filter(status= "Accepted")
    context = {'order':order}
    return render(request,'order/accepted.html',context)


def delivered(request):
    order = OrderPlaced.objects.filter(status= "Delivered")
    context = {'order':order}
    return render(request,'order/delivered.html',context)


def canceled(request):
    order = OrderPlaced.objects.filter(status= "Canceled")
    context = {'order':order}
    return render(request,'order/canceled.html',context)


def vieworder(request,id):
    order = OrderPlaced.objects.get(id = id)
    context = {'order':order}
    return render(request,'order/orderview.html',context)


def changestatus(request):
    if request.method =="POST":
        oid = request.POST['oid']
        status= request.POST['status']
        order = OrderPlaced.objects.get(id = oid)
        order.status = status
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))