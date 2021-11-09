from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import *
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from . utils import cookieCart, cartData, guestOrder


class StoreView(View):
    def get(self, request):

        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=request.user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.all_cart_quantity
        else:
            items = []
            order = {'all_cart_value':0,'all_cart_quantity':0, 'shipping':False}
            cartItems = order['all_cart_quantity']
        products=Product.objects.all()
        context={'products':products, 'cartItems':cartItems}
        return render(request, 'store/store.html', context)


class About(View):
    def get(self,request):
        context={}
        return render(request, 'store/about.html', context)

class CartView(View):
    def get(self, request):

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'items': items, 'order':order, 'cartItems':cartItems}
        return render(request, 'store/cart.html', context)

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.all_cart_quantity
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    context = {'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer=request.user
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created= OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)

    elif action =='remove':
        orderItem.quantity=(orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if request.POST["password"] == request.POST["password_confirmation"]:

                # user = User.objects.get(id=request.user.id)
                print(form.is_valid())
                if form.is_valid():
                    # user.username = form.cleaned_data.get('username')
                    # user.email = form.cleaned_data.get('email')
                    # user.save()
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )
                    print("Here")
                    messages.success(request, 'Account was created for {}'.format(user))
                    return redirect('store')
                else:
                    messages.error(request, 'Data is invalid')
                    return redirect('store')

            else:
                messages.error(request, 'Passwords are not the same.')
                return redirect('store')

        context = {'form': form}
        return render(request, 'store/register.html', context)


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
    return render(request, 'store/login.html', {'page':page})


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.all_cart_value:
            order.complete = True
        order.save()


    else:
        total, order=guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.all_cart_value:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            postcode=data['shipping']['postcode'],
        )
    return JsonResponse('Payment submitted..', safe=False)

# Create your views here.

