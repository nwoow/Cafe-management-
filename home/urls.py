from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.home,name='home'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('generateqr',views.generateqr,name='generateqr'),
    path('viewqr/<int:id>',views.viewqr,name='viewqr'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('delcategory/<int:id>',views.delcategory,name='delcategory'),
    # path('addsubcategory',views.addsubcategory,name='addsubcategory'),
    # path('delsubcategory/<int:id>',views.delsubcategory,name='delsubcategory'),
    path('addmenu',views.addmenu,name='addmenu'),
    path('delmenu/<int:id>',views.delmenu,name='delmenu'),
    path('delqr/<int:id>',views.delqr,name='delqr'),

    path('menu/',views.viewmenu,name='viewmenu'),
    path('viewmenuview/',views.viewmenuview,name='viewmenuview'),

    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart,name='cart'),
    path('delcart/<id>',views.delcart,name='delcart'),

    path('placeorder',views.placeorder,name='placeorder'),
    path('vieworderdet',views.vieworderdet,name='vieworderdet'),
    path('pending',views.pending,name='pending'),
    path('accepted',views.accepted,name='accepted'),
    path('delivered',views.delivered,name='delivered'),
    path('canceled',views.canceled,name='canceled'),
    path('vieworder/<id>',views.vieworder,name='vieworder'),
    path('changestatus',views.changestatus,name='changestatus'),
]