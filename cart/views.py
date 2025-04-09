from decimal import Decimal
from django.views import View
from .cart_module import Cart
from django.urls import reverse
from .forms import AddAddressForm
from product.models import Product
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Address, DiscountCode
from django.shortcuts import render, redirect, get_object_or_404


class CartDetail(LoginRequiredMixin, View):
    login_url = 'account:check-username'

    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/checkout-cart.html', {'cart': cart})


class CartAdd(View):
    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        if not size or not color or not quantity:
            messages.error(request, "لطفاً همه گزینه‌ها را انتخاب کنید.")
            return redirect(reverse('product:product_detail', args=[product.slug]))
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "تعداد وارد شده معتبر نیست.")
            return redirect(reverse('product:product_detail', args=[product.slug]))
        cart.add(product=product, quantity=quantity, color=color, size=size)
        messages.success(request, "محصول به سبد خرید اضافه شد.")
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


class CartShipping(LoginRequiredMixin, View):
    login_url = 'account:check-username'

    def get(self, request):
        cart = Cart(request)
        form = AddAddressForm()
        return render(request, 'cart/checkout-shipping.html', {'cart': cart, 'form': form})

    def post(self, request):
        form = AddAddressForm(request.POST)
        if form.is_valid():
            Address.objects.filter(user=request.user).delete()
            cd = form.cleaned_data
            Address.objects.create(
                user=request.user,
                full_name=cd['full_name'],
                phone=cd['phone'],
                address=cd['address'],
                city=cd['city'],
                province=cd['province'],
                zip_code=cd['zip_code'],
            )
            messages.success(request, "آدرس شما با موفقیت ذخیره شد.")
            return redirect('cart:cart_shipping')
        messages.error(request, "لطفاً تمام فیلدها را به درستی پر کنید.")
        return render(request, 'cart/checkout-shipping.html', {'form': form})


class CartPayment(LoginRequiredMixin, View):
    login_url = 'account:check-username'

    def get(self, request, pk):
        cart = Cart(request)
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/checkout-payment.html', {'cart': cart, 'order': order})


class OrderCreation(View):
    def get(self, request):
        cart = Cart(request)
        if cart.total_products == 0:
            messages.error(request, "سبد خرید شما خالی است.")
            return redirect('cart:cart_detail')
        Order.objects.filter(user=request.user, is_paid=False).delete()
        order = Order.objects.create(user=request.user, total_price=int(cart.total_price()))
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                color=item.get('color'),
                size=item.get('size'),
                quantity=item['quantity'],
                price=item['price']
            )
        messages.success(request, "سفارش با موفقیت ایجاد شد.")
        return redirect('cart:cart_payment', order.id)


class ApplyDiscount(View):
    def post(self, request, pk):
        code = request.POST.get('discount')
        order = get_object_or_404(Order, id=pk)
        if order.discount_applied:
            messages.warning(request, "کد تخفیف قبلاً اعمال شده.")
            return redirect('cart:cart_payment', order.id)
        discount = get_object_or_404(DiscountCode, name=code)
        if discount.quantity <= 0:
            messages.error(request, "کد تخفیف معتبر نیست.")
            return redirect('cart:cart_payment', order.id)
        discount_amount = (order.total_price * Decimal(discount.discount)) / Decimal('100')
        order.total_price -= discount_amount
        order.discount_applied = True
        order.save()
        discount.quantity -= 1
        discount.save()
        messages.success(request, f"کد تخفیف {code} با موفقیت اعمال شد.")
        return redirect('cart:cart_payment', order.id)
