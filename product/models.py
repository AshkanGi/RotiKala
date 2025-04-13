import random
from slugify import slugify
from django.db import models
from account.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator


class Attribute(models.Model):
    name = models.CharField(max_length=100, verbose_name="عنوان ویژگی")

    def __str__(self):
        return self.name


class BooleanAttribute(models.Model):
    name = models.CharField(max_length=100, verbose_name='عنوان ویژگی')

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="values", verbose_name='عنوان ویژگی')
    value = models.CharField(max_length=100, verbose_name="مقدار ویژگی")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='subs', verbose_name='زیر مجموعه')
    title = models.CharField(max_length=100, verbose_name='عنوان')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name='دسته بندی')
    name = models.CharField(max_length=150, verbose_name='نام محصول')
    main_image = models.ImageField(upload_to='product/main', verbose_name='عکس اصلی')
    description = RichTextUploadingField(null=True, blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='اخرین تغییرات')
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True, verbose_name='نامک')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت')
    discount_percentage = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='تخفیف (%)'
    )

    @property
    def discounted_price(self):
        price = self.price * (1 - self.discount_percentage / 100)
        if self.discount_percentage:
            return format(price).rstrip('0').rstrip('.')
        return price

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            number = random.randint(10000, 99999)
            slug = f'{base_slug}-{number}'
            while Product.objects.filter(slug=slug).exists():
                number = random.randint(10000, 99999)
                slug = f'{base_slug}-{number}'
            self.slug = slug
        super().save()

    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images', verbose_name='محصول', null=True, blank=True)
    image = models.ImageField(upload_to='product/gallery', verbose_name='تصویر گالری')
    alt_text = models.CharField(max_length=100, blank=True, null=True, verbose_name='عنوان عکس')

    def __str__(self):
        return self.alt_text or f"تصویر {self.id} از {self.product.name}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes", verbose_name='محصول')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, verbose_name='مقدار ویژگی')

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value}"


class ProductBooleanAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='boolean_attributes', verbose_name='محصول')
    attribute = models.ForeignKey(BooleanAttribute, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.BooleanField(default=False, verbose_name='مقدار ویژگی')

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {'✅' if self.value else '❌'}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    title = models.CharField(max_length=40, null=True, blank=True, verbose_name='عنوان')
    body = models.TextField(verbose_name='متن')
    is_recommended = models.BooleanField(default=False, verbose_name='توصیه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f'{self.user.username} : {self.title}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', verbose_name='محصول')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f'{self.user} liked {self.product}'
