from django.contrib import messages
from .forms import CommentCreatForm
from .models import Product, Comment
from cart.cart_module import Cart
from django.shortcuts import redirect
from django.views.generic import DetailView


class ProductView(DetailView):
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreatForm()
        context['cart'] = Cart(self.request)
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = CommentCreatForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment()
            comment.user = request.user
            comment.product = product
            comment.title = cd['title']
            comment.body = cd['body']
            recommend_value = request.POST.get('recommend')
            if recommend_value is not None:
                comment.is_recommended = bool(int(recommend_value))
            else:
                comment.is_recommended = False
            comment.save()
            return redirect('ProductApp:product_detail', slug=product.slug)
        messages.error(request, 'اطلاعات وارد شده مناسب  نیست , لطفا مجدد تلاش کنید.')
        return self.get(request, *args, **kwargs)