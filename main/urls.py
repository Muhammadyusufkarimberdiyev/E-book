from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'main'

urlpatterns = [
    path('',register,),
    path('login',Login,),
    path('home', HomepageView.as_view(), name='home'),
    path('', Book_View.as_view(), name='books'),
    path('search', search, name="search"),
    path("category/<int:category_id>",
         CategoryView.as_view(), name="category"),
    path('contant', ContantpageView.as_view(), name='contant'),
    path('Read/<int:article_id>', Read.as_view(), name='Read'),
    path('adetail/<int:article_id>', adetail.as_view(), name='adetail'),
    path('back', backpageView.as_view(), name='back'),
    path('register',register,),
     path('logout/', LogoutPage, name='logout'), 
    path("add/<int:book_id>", Add_Cart.as_view(), name="add_to_cart"),
    path("cart/remove/<int:cart_id>/", Remove_Cart.as_view(), name="remove_from_cart"),
    path("favorites/", view_favorites, name="favorites"),
    path("Fadd/<int:book_id>/", Fav_add.as_view(), name="add_to_favorites"),
    path("payment/", process_payment, name="process_payment"),
    path("payment/success/<str:transaction_id>/", payment_success, name="payment_success"),
    path('cart/', view_cart, name='cart'),  
    path('add-cart/<int:book_id>/', Add_Cart.as_view(), name='add_cart'),
    path('remove-cart/<int:cart_id>/', Remove_Cart.as_view(), name='remove_cart'),
    path('update-cart/<int:item_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove-cart-ajax/<int:item_id>/', remove_cart, name='remove_cart_ajax'),
    path("cart/update/<int:item_id>/<str:action>/", update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_cart"),
    path("favorites/remove/<int:item_id>/", remove_favorite, name="remove_favorite"),
    path("home/", save_comment, name="home"),
    # path("cart/add/<int:book_id>/", add_to_cart, name="add_to_cart"),
]
