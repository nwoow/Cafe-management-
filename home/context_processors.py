from . models import *

def food_in_cart(request):
    cart = request.session.get('cart') 
    food = []
    totalamount = 0
    if cart:
        for k in cart:
            queryset =Food.objects.filter(id=k).first()
            queryset.quantity = cart[k]
            totalamount = totalamount + (queryset.price*int(queryset.quantity))
            food.append(queryset)  
    return {'food_in_cart':food,'totalamount':totalamount,'cart_count':len(food)}



def order_detail_processor(request):
    pending_order_det = OrderPlaced.objects.filter(status='Pending').count()
    accepted_order_det = OrderPlaced.objects.filter(status='Accepted').count()
    completed_order_det = OrderPlaced.objects.filter(status='Delivered').count()
    canceled_order_det = OrderPlaced.objects.filter(status='Canceled').count()
    return {
        'pending_order_det':accepted_order_det,
        'accepted_order_det':accepted_order_det,
        'completed_order_det':completed_order_det,
        'canceled_order_det':canceled_order_det
    }
