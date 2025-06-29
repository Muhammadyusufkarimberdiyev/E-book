
from django.views import *
from .models import *
from ast import arg
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse,HttpResponse
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import book, CartItem, Favorite, Payment
import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



class HomepageView(View):

    def get(self, request):
        c = Category.objects.all()
        b=book.objects.all()
        e=audio.objects.all()
        a=Comment.objects.all()
        d=book_category.objects.all()
        f=CartItem.objects.all()
        o=Favorite.objects.all()
        context = {
            "contant": a,
            "category": c,
            "books":b,
            "bcategory":d,
            "audio":e,
            "cart":f,
            "favo":o
        }
        return render(request, 'index.html',context)




class ContantpageView(View):
    def get(self, request):
        return render(request, 'index.html',)


class Read(View):
    def get(self, request, article_id):
        c = Category.objects.all()
        d=book_category.objects.all()
        a = book.objects.get(id=article_id)
        context = {
            "i": a,
            "bcategory": d,
            "category": c,

        }
        return render(request, 'detail.html', context)



class adetail(View):
    def get(self, request, article_id):
        c = Category.objects.all()
        d=book_category.objects.all()
        a = audio.objects.get(id=article_id)
        context = {
            "i": a,
            "bcategory": d,
            "category": c,

        }
        return render(request, 'adetail.html', context)


def search(request):
    query = request.POST.get('q')
    print(query)
    categories = Category.objects.all()
    q = Q(title__contains=query) | Q(category__name__contains=query)
    
    a = book.objects.filter(q)
    c=audio.objects.filter(q)
    context = {
        "books": a,
        "categorys": categories,
        "audios": a,
    }
    return render(request, "index.html", context)



@login_required
def view_cart(request):
    """Savatchani ko‘rish"""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def update_cart(request, item_id, action):
    """Savatchadagi mahsulot sonini oshirish yoki kamaytirish"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({"success": True})



@csrf_exempt
def update_cart(request, item_id, action):
    if request.method == "POST":
        try:
            cart_item = CartItem.objects.get(id=item_id)
            if action == "increase":
                cart_item.quantity += 1
            elif action == "decrease" and cart_item.quantity > 1:
                cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@csrf_exempt
def remove_from_cart(request, item_id):
    if request.method == "POST":
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@login_required
def remove_cart(request, item_id):
    """Savatchadan mahsulotni o‘chirish (AJAX)"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return JsonResponse({"success": True})


class Add_Cart(View):
    """Mahsulotni savatchaga va sevimlilarga qo‘shish"""

    @method_decorator(login_required)
    def get(self, request, book_id):
        book_obj = get_object_or_404(book, id=book_id)

      
        cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book_obj)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

       
        Favorite.objects.get_or_create(user=request.user, book=book_obj)
     
        return view_cart(request) 

@login_required
def view_cart(request):
    """Savatchani ko‘rish"""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})




class Remove_Cart(View):
    @login_required
    def remove_from_cart(request, cart_id):
        cart_item = get_object_or_404(CartItem, id=cart_id, user=request.user)
        cart_item.delete()
        return redirect("cart")



class Fav_add(View):
    """Mahsulotni sevimlilarga qo‘shish va ko‘rish"""

    @method_decorator(login_required)
    def get(self, request, book_id):
        book_obj = get_object_or_404(book, id=book_id)
        Favorite.objects.get_or_create(user=request.user, book=book_obj)

        return view_favorites(request)  

@login_required
def view_favorites(request):
    """Sevimlilar sahifasini ko‘rish"""
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, "favorites.html", {"favorites": favorites})


@csrf_exempt
def remove_favorite(request, item_id):
    if request.method == "POST":
        try:
            favorite_item = Favorite.objects.get(id=item_id)
            favorite_item.delete()
            return JsonResponse({"success": True})
        except Favorite.DoesNotExist:
            return JsonResponse({"success": False, "error": "Item not found"})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

@csrf_exempt
def add_to_cart(request, book_id):
    if request.method == "POST":
        try:
            cart_item, created = CartItem.objects.get_or_create(book_id=book_id)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


@login_required
def process_payment(request):
    """Foydalanuvchini Click to‘lov sahifasiga yo‘naltiradi."""
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if total_price == 0:
        return HttpResponse("Mahsulot narxi nolga teng", status=400)

    transaction_id = str(uuid.uuid4())

    payment = Payment.objects.create(
        user=request.user,
        amount=total_price,
        transaction_id=transaction_id,
        status="pending"
    )

    click_api_url = f"https://my.click.uz/payment?amount={total_price}&transaction_id={transaction_id}&user_id={request.user.id}"
    # click_api_url="https://click.uz/ru"
    return redirect(click_api_url)  



@login_required
def payment_success(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    payment.status = "completed"
    payment.save()


    CartItem.objects.filter(user=payment.user).delete()
    
    return render(request, "payment_success.html", {"payment": payment})



def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/home') 
        else:
       
            return render(request, 'login.html', {'error': 'Username or Password is incorrect!'})

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
       
        if User.objects.filter(username=uname).exists():
            return render(request, 'register.html', {'error': 'Username already exists!'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists!'})

        my_user = User.objects.create_user(uname, email, password)
        my_user.save()
        return redirect('/login')

    return render(request, 'register.html')

def LogoutPage(request):
    logout(request)
    return redirect('/')

def book_list(request):
    books = book.objects.all()
    paginator = Paginator(books, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'page_obj': page_obj})


class Book_View(View):

    def get(self, request):
        articles = book.objects.all()
        paginator = Paginator(articles, 3)

        num_page = request.GET.get('page', 1)
        page = paginator.get_page(int(num_page))

        article = book.objects.first()
        categories = Category.objects.all()

        context = {
            "articles": page.object_list,
            "page": page,
            "category": categories,
            "article": article,
            "paginator": paginator,
        }

        return render(request, 'index.html', context)

    def post(self, request):
        categories = Category.objects.all()

        query = request.POST.get('q', '').strip()  # Bo'sh qidiruvni oldini olish uchun
        if not query:
            return redirect('home')  # Agar foydalanuvchi hech narsa yozmasa, bosh sahifaga qaytadi

        q = Q(name__icontains=query) | Q(category__name__icontains=query)
        results = book.objects.filter(q)

        context = {
            "articles": results,
            "category": categories,
            "message": "Bunday kitob topilmadi" if not results.exists() else ""
        }
        return render(request, "index.html", context)

class CategoryView(View):

    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        categorys = Category.objects.all()

        articles = book.objects.filter(category=category)
   
        context = {"category": categorys, "books": articles }
        return render(request, "index.html", context)




class backpageView(View):

    def get(self, request):
        c = Category.objects.all()
        b=book.objects.all()
        e=audio.objects.all()
        a=Comment.objects.all()
        d=book_category.objects.all()
        context = {
            "contant": a,
            "category": c,
            "books":b,
            "bcategory":d,
            "audio":e
        }
        return render(request, 'index.html',context)
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def save_comment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        text = request.POST.get("message")

        if name and email and text:
            try:
                Comment.objects.create(name=name, email=email, text=text)
                logger.info("Comment saqlandi!")
                return redirect('/home')
            except Exception as e:
                logger.error(f"Xatolik: {e}")
                return render(request, "index.html", {"error": "Bazaga yozishda xatolik yuz berdi!"})

    return render(request, "index.html")