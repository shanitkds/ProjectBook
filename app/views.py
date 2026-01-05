from django.shortcuts import render,redirect,get_object_or_404
from .models import Book,Cart
from .forms import BookForm,CustomUseRCreationForm,LoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.urls import reverse

stripe.api_key=settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    return render(request,"home.html")

def viewBook(request):
    book=Book.objects.all()
    return render(request,"viewbook.html",{"b":book})

@login_required
def create_book(request):
    form=BookForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('viewbook')
    return render(request,'createBook.html',{"form":form})

@login_required
def update(request,id):
    book=Book.objects.get(id=id)
    form=BookForm(request.POST or None,request.FILES or None,instance=book)
    if form.is_valid():
        form.save()
        return redirect('viewbook')
    return render(request,'update_book.html',{'form':form})

@login_required
def delete(request,id):
    book=get_object_or_404(Book,id=id)
    if request.method=='POST':
        book.delete()
        return redirect('viewbook')
    return render(request,'delete.html',{'book':book})


def register_view(request):
    form=CustomUseRCreationForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save() 
        return redirect('viewbook')
    return render(request,'register.html',{'form':form})

def login_view(request):
    form=LoginForm(request, data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.get_user()
        login(request, user)
        return redirect('viewbook')
    return render(request,'Login.html',{"form":form})

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def add_cart(request,book_id):
    book=get_object_or_404(Book,id=book_id)
    cart_item,created=Cart.objects.get_or_create(user=request.user,book=book)
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('viewcart')

@login_required
def view_cart(request):
    orders=Cart.objects.filter(user=request.user)
    for i in orders:
        i.book.price=i.book.price*i.quantity
    return render(request,'view_cart.html',{'order':orders})

def cart_remove(request,re_id):
    book=get_object_or_404(Cart,id=re_id,user=request.user)
    if book.quantity >1:
        book.quantity-=1
        book.save()
    else:
        book.delete()
    return redirect('viewcart')
        
        
def buy_now(request,book_id):
    cart_item=Cart.objects.filter(user=request.user,book_id=book_id)
    if not cart_item.exists():
        return redirect('viewcart')
    book=get_object_or_404(Book,id=book_id)
    total_quantity=sum(item.quantity for item in cart_item)
    
    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
            'price_data':{
                'currency':'inr',
                'product_data':{
                    'name':book.name,
                },
                'unit_amount':int(float(book.price)*100),
            },
            'quantity':total_quantity
            }
        ],
        mode='payment',
        
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('cancel')),
        
    )
    
    return redirect(session.url)
    
def success(request):
    return render(request,'susess.html')
def cancel(request):
    return redirect(request,'cancel.html')