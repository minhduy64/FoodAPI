from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    avatar = CloudinaryField()


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=30, default='tag')

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Store(BaseModel):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = RichTextField()
    image = CloudinaryField()
    location = models.CharField(max_length=255)
    categories = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} - {self.location}"


class MenuItem(BaseModel):
    name = models.CharField(max_length=255)
    content = RichTextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = CloudinaryField()
    price = models.DecimalField(max_digits=20, decimal_places=0)
    available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.store}"


class InteractionMenuItem(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class InteractionStore(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ReviewMenuItem(InteractionMenuItem):
    content = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def save(self, *args, **kwargs):
        if self.menu_item.available and self.menu_item.store == self.store:
            super().save(*args, **kwargs)
        else:
            raise ValueError("The menu item is not available in the store.")

    def __str__(self):
        return f"Review for {self.menu_item.name} by {self.user.username} ({self.store})"


class ReviewStore(InteractionStore):
    content = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return f"Review for {self.store} by {self.user.username}"


class LikeMenuItem(InteractionMenuItem):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('menu_item', 'user')


class LikeStore(InteractionStore):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('store', 'user')

# class Order(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(MenuItem, through='OrderItem')
#     total_amount = models.DecimalField(max_digits=20, decimal_places=2)
#     payment_method = models.CharField(max_length=50)
#
#     def __str__(self):
#         return f"Order #{self.id} - User: {self.user}"
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return f"{self.quantity} x {self.item}"
#
#
# class Review(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     comment = models.TextField()
#
#     def __str__(self):
#         return f"Review for {self.restaurant} by {self.user}"
