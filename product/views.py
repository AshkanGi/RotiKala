from django.views import View
from django.contrib import messages
from .forms import CommentCreatForm
from .models import Product, Comment, Like
from django.views.generic import DetailView
from django.shortcuts import redirect, get_object_or_404


class ProductView(DetailView):
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreatForm()
        product = self.get_object()
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
                comment.title = cd.get('title')
                comment.body = cd.get('body')
                recommend_value = request.POST.get('recommend')
                if recommend_value:
                    comment.is_recommended = bool(int(recommend_value))
                else:
                    comment.is_recommended = False
                comment.save()
                messages.success(request, 'نظر شما با موفقیت ثبت شد، ممنونیم 🌟')
                return redirect('product:product_detail', slug=product.slug)
            messages.error(request, 'اطلاعات وارد شده مناسب  نیست , لطفا مجدد تلاش کنید.')
        messages.error(request, 'برای ثبت نظر باید وارد حساب کاربری خودتان شوید.')
        return self.get(request, *args, **kwargs)


class LikeView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            messages.error(request, 'برای لایک کردن باید وارد حساب کاربری شوید.')
            return redirect('product:product_detail', slug=slug)
        product = get_object_or_404(Product, slug=slug)
        like, created = Like.objects.get_or_create(product=product, user=request.user)
        if not created:
            like.delete()
        return redirect('product:product_detail', slug=slug)
