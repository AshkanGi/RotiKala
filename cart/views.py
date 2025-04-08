from django.contrib import messages
from django.views import View
from .cart_module import Cart
from .forms import AddAddressForm
from product.models import Product
from .models import Order, OrderItem, Address, DiscountCode
from django.shortcuts import render, redirect, get_object_or_404


class CartDetail(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/checkout-cart.html', {'cart': cart})


class CartAdd(View):
    def post(self, request, pk):
        cart = Cart(request)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, id=pk)
        cart.add(product, quantity, color, size)
        return redirect('cart:cart_detail')


class CartRemove(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.remove(id)
        return redirect('cart:cart_detail')


class CartClear(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect('cart:cart_detail')


class CartShipping(View):
    def get(self, request):
        cart = Cart(request)
        form = AddAddressForm()
        return render(request, 'cart/checkout-shipping.html', {'cart': cart, 'form': form})

    def post(self, request):
        form = AddAddressForm(request.POST)
        if form.is_valid():
            Address.objects.filter(user=request.user).delete()
            form.save(user=request.user)
            messages.success(request, "آدرس شما با موفقیت ذخیره شد.")
            return redirect('cart:cart_shipping')
        messages.error(request, "لطفاً تمام فیلدها را به درستی پر کنید.")
        return render(request, 'cart/checkout-shipping.html', {'form': form})


class CartPayment(View):
    def get(self, request, pk):
        cart = Cart(request)
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/checkout-payment.html', {'cart': cart, 'order': order})


class OrderCreation(View):
    def get(self, request):
        cart = Cart(request)
        Order.objects.filter(user=request.user).delete()
        order = Order.objects.create(user=request.user, total_price=int(cart.total_price()))
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'], size=item['size'], quantity=item['quantity'], price=item['price'])
        return redirect('cart:cart_payment', order.id)


class ApplyDiscount(View):
    def post(self, request, pk):
        code = request.POST.get('discount')
        order = get_object_or_404(Order, id=pk)
        discount = get_object_or_404(DiscountCode, name=code)
        order.total_price -= order.total_price * discount.discount/100
        order.save()
        discount.quantity -= 1
        discount.save()
        return redirect('cart:cart_payment', order.id)
