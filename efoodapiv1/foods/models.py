from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    is_store_owner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    user_location = models.CharField(max_length=255, null=True)#,default='Quan 1')
    user_latitude = models.CharField(max_length=255, null=True)#,default='10.765505130395395')
    user_longitude = models.CharField(max_length=255, null=True)#,default='106.68168869289711')

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    icon = CloudinaryField(max_length=1024)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Store(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = RichTextField()
    image = CloudinaryField()
    location = models.CharField(max_length=255)
    categories = models.ForeignKey(Category, on_delete=models.PROTECT)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    @property
    def rating(self):
        reviews_count = self.reviews.count()
        if reviews_count > 0:
            avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(avg_rating, 1)
        else:
            return 0.0

    def __str__(self):
        return f"{self.name} - {self.location}"


class MenuItem(BaseModel):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    content = RichTextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = CloudinaryField()
    price = models.DecimalField(max_digits=20, decimal_places=0)
    available = models.BooleanField(default=True)
    sell_start_time = models.TimeField()
    sell_end_time = models.TimeField()
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.store}"


class InteractionBase(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(InteractionBase):
    content = models.CharField(max_length=255)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment for {self.menu_item.name} by {self.user.username}"


class ReviewMenuItem(InteractionBase):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="review_menu")
    content = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return f"Review by {self.user.username} on {self.menu_item.name}"


class ReviewStore(InteractionBase):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews')
    content = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return f"Review for {self.store.name} - {self.store.location} by {self.user.username}"


class LikeMenuItem(InteractionBase):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('menu_item', 'user')

    def __str__(self):
        return f"Likes for {self.menu_item}"


class LikeStore(InteractionBase):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('store', 'user')


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=20, decimal_places=0)
    delivery_fee = models.DecimalField(max_digits=20, decimal_places=0)
    payment_method = models.CharField(max_length=20, choices=[('paypal', 'PayPal'), ('stripe', 'Stripe'),
                                                              ('momo', 'MoMo'), ('zalopay', 'Zalo Pay'),
                                                              ('cash', 'Cash')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'),
                                                      ('delivered', 'Delivered')], default='pending')

    def __str__(self):
        return f"Order #{self.id} - User: {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Order #{self.order.id}"


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.sent_at}"


class RevenueReport(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=20, decimal_places=0)
    report_date = models.DateField()

    def __str__(self):
        return f"Revenue Report for {self.store.name} on {self.report_date}"


class AdminRevenueReport(BaseModel):
    total_revenue = models.DecimalField(max_digits=20, decimal_places=0)
    report_date = models.DateField()

    def __str__(self):
        return f"Admin Revenue Report on {self.report_date}"
