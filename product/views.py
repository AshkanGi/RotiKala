from django.contrib import messages
from .forms import CommentCreatForm
from .models import Product, Comment
#from cart.cart_module import Cart
from django.shortcuts import redirect
from django.views.generic import DetailView


class ProductView(DetailView):
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreatForm()
        product = self.get_object()
        #context['cart'] = Cart(self.request)
        product_categories = product.category.all()
        related_products = Product.objects.filter(category__in=product_categories).exclude(id=product.id).distinct()
        context['related_products'] = related_products
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = CommentCreatForm(request.POST)
        if request.user.is_authenticated:
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
        messages.error(request, 'برای ثبت نظر باید وارد اکانت خودتان شوید.')
        return self.get(request, *args, **kwargs)
