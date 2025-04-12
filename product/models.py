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


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=100, verbose_name="مقدار ویژگی")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='subs')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    image = models.ImageField(upload_to='product/gallery', verbose_name='گالری')
    alt_text = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.alt_text


class Product(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=150, unique=True, verbose_name='نام محصول')
    main_image = models.ImageField(upload_to='product/main', verbose_name='عکس اصلی')
    gallery_image = models.ManyToManyField(ProductGallery, related_name='product', verbose_name='گالری')
    description = RichTextUploadingField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
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

    class Meta:
        ordering = ['-created_at']


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=40, null=True, blank=True)
    body = models.TextField()
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} : {self.title}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.product}'
