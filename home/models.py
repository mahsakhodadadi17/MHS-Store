from django.db import models 
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    date = models.DateTimeField()
    price = models.PositiveIntegerField(verbose_name="قیمت تومان")
    discount = models.PositiveIntegerField(default=0)
    mojodi = models.BooleanField(default=False)
    image = models.ImageField(upload_to='home/')
    email = models.EmailField()
    order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    show_in_new = models.BooleanField(default=False)

    slug = models.CharField(max_length=200, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
     if not self.slug:
        super().save(*args, **kwargs)

        english_slug = {
            "کتونی زنانه": "women-sneakers",
            "کتونی مردانه": "men-sneakers",
            "کفش زنانه": "women-shoes",
            "کفش مردانه": "men-shoes",
            "صندل زنانه": "women-sandals",
        }

        self.slug = f"{english_slug.get(self.title, 'product')}-{self.id}"

        super().save(update_fields=["slug"])
     else:
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        return self.price - (self.price * self.discount / 100)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
   name=models.CharField()
   email=models.EmailField()
   message=models.TextField()




class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )


    image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )


    def __str__(self):

        return self.user.username






class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    product = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.user.username
    


class Address(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    city = models.CharField(
        max_length=100
    )

    address = models.TextField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.full_name
    
class Order(models.Model):

    STATUS = (
        ("pending","در انتظار"),
        ("paid","پرداخت شده"),
        ("sent","ارسال شده"),
        ("done","تحویل داده شده"),
        ("cancelled","لغو شده"),
    )


    PAYMENT_STATUS = (
        ("unpaid","پرداخت نشده"),
        ("paid","پرداخت شده"),
    )


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    total_price = models.IntegerField()


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )


    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="unpaid"
    )

    admin_seen = models.BooleanField(
     default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



    def can_cancel(self):

        return (
            timezone.now()
            <= self.created_at + timedelta(hours=24)
            and self.status in ["pending","paid"]
        )



    def save(self, *args, **kwargs):

        if self.pk:

            old_order = Order.objects.get(
                pk=self.pk
            )


            if old_order.status != self.status:

                super().save(*args, **kwargs)


                Notification.objects.create(

                    user=self.user,

                    text=f"وضعیت سفارش شماره {self.id} تغییر کرد به {self.get_status_display()}"

                )


                return


        super().save(*args, **kwargs)




    def __str__(self):

        return f"Order {self.id}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.IntegerField()


    def total_price(self):

        return self.price * self.quantity


    def __str__(self):

        return self.product.title   
    

class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )


    product = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )


    quantity = models.PositiveIntegerField(
        default=1
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(
     default=False
    )

    def __str__(self):
        return self.text
    

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="profile/",
        default="profile/default.png"
    )


    def __str__(self):
        return self.user.username
    

class ContactMessage(models.Model):

    MESSAGE_TYPES = (
        ("general", "سوال عمومی"),
        ("order", "مشکل سفارش"),
    )


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default="general"
    )


    order_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


    subject = models.CharField(
        max_length=200
    )


    message = models.TextField()


    is_read = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.subject
    
class ContactMessage(models.Model):

    MESSAGE_TYPES = (
        ("general", "سوال عمومی"),
        ("order", "مشکل سفارش"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default="general"
    )

    order_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=(
          ("open", "باز"),
         ("answered", "پاسخ داده شده"),
         ("closed", "بسته شده"),
        ),
        default="open"
    )

    def __str__(self):
        return self.subject


class TicketReply(models.Model):

    contact = models.ForeignKey(
        ContactMessage,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_admin = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.message[:40]
    

class AdminNotification(models.Model):

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title