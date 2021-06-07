from django.urls import path
from . import views
from .views import *
from django.conf.urls import url



urlpatterns=[
    path('',views.main,name='main'),
    path('home/',views.products,name='home'),
    path('login/',views.loginview,name='login'),
    path('signup/',views.signup,name='signup'),
    path('orderh/',views.orderhistory,name='orderh'),
    path('profile/',views.updateprofile_view,name='profile'),
    path('cart/',views.usercart,name='cart'),
    path('signup/login/',views.loginview,name='login'),
    path('login/home/',views.products,name='home'),
    path('signup/home/',views.products,name='home'),
    path('signup/login/home/',views.products,name='home'),
    path('logout/', views.logout_view, name="logout"),
    path('logout/main/',views.main,name="main"),
    path('login/viewproduct/addproduct/',views.addproductform,name='addproduct'),
    path('login/viewproduct/',views.viewproduct,name='view'),
    path('login/viewproduct/addproduct/viewproduct/',views.viewproduct),
    path('update/<id>',views.updateproduct,name='update'),
    path('delete/<id>',views.deleteproduct,name='delete'),
    path('cloth/',views.clothes,name='cloth'),
    path('electronics/',views.electronics,name='elec'),
    path('book/',views.books,name='book'),
    path('shoes/',views.shoes,name='shoes'),
    path('signup/login/viewproduct/',views.viewproduct,name='view'),
    path('viewdesc/<id>',views.product_detail,name='product_detail'),
    # path('cart/',views.usercart,name='cart'),
    # path('cart/<id>',views.usercarttt,name='ucart'),
    path('orderhistory',views.orderhistory,name='orderhistory'),
    path('shipping',views.shipping,name='shipping'),
    path('contact/',views.contact,name='contact'),
    path('signup/login/viewuser/',views.viewuser,name='viewuser'),
    path('shipping/<id>/',views.shipping,name='shipping'),
    path('signup/login/viewproduct/',views.viewproduct,name='viewproduct'),
    path('vcloth/',views.vclothes,name='vcloth'),
    path('velectronics/',views.velectronics,name='velec'),
    path('vbook/',views.vbooks,name='vbook'),
    path('vshoes/',views.vshoes,name='vshoes'),
    path('orders/',views.vieworder,name='order'),
    # url(r'^$', views.cart_detail, name='cart_detail'),
    # url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    path('add/<id>',views.cart_add,name='cart_add'),
    path('usercart/',views.cart_detail,name='cart_detail'),
    path('remove/<id>',views.cart_remove,name='cart_remove'),
    path('pd/<id>', views.product_detail, name='product_detail'),
    # url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    # url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
