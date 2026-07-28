from rest_framework import serializers
from .models import Post
from .models import Wishlist
from .models import Cart, CartItem
from .models import Profile
from .models import Order, OrderItem
from .models import Address
from .models import Notification
from rest_framework import serializers
from .models import ContactMessage, TicketReply
from .models import Coupon
from .models import AdminTask
from .models import Discount
from django.contrib.auth.models import User
from .models import Category
from .models import SiteSettings
from .models import Banner



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "قیمت نمی‌تواند منفی باشد."
            )
        return value



class WishlistSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    product_price = serializers.IntegerField(
        source="product.price",
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "product",
            "product_title",
            "product_price",
            "product_image",
            "created_at",
        ]


class CartItemSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    product_price = serializers.IntegerField(
        source="item_price",
        read_only=True
    )

    total_price = serializers.IntegerField(
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_title",
            "product_image",
            "color",
            "size",
            "quantity",
            "product_price",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        source="cartitem_set",
        many=True,
        read_only=True
    )

    total_price = serializers.SerializerMethodField()


    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
            "created_at",
        ]


    def get_total_price(self, obj):
        return sum(
            item.total_price
            for item in obj.cartitem_set.all()
        )

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "phone",
            "image",
        ]


class OrderItemSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    total_price = serializers.IntegerField(
        read_only=True
    )


    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_title",
            "quantity",
            "price",
            "total_price",
            "color",
            "size",
        ]



class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )


    class Meta:
        model = Order
        fields = [
            "id",
            "address",
            "total_price",
            "final_price",
            "status",
            "payment_status",
            "tracking_code",
            "items",
            "created_at",
        ]

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            "id",
            "full_name",
            "phone",
            "city",
            "address",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            "id",
            "text",
            "is_read",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

class TicketReplySerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = TicketReply

        fields = [
            "id",
            "username",
            "message",
            "is_admin",
            "created_at",
        ]


class TicketSerializer(serializers.ModelSerializer):

    replies = TicketReplySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ContactMessage

        fields = [
            "id",
            "message_type",
            "order_id",
            "subject",
            "message",
            "status",
            "is_read",
            "created_at",
            "replies",
        ]

class CouponApplySerializer(serializers.Serializer):

    code = serializers.CharField()


class AdminDashboardSerializer(serializers.Serializer):
    orders_count = serializers.IntegerField()
    products_count = serializers.IntegerField()
    users_count = serializers.IntegerField()
    total_revenue = serializers.IntegerField()

    pending_orders = serializers.IntegerField()
    paid_orders = serializers.IntegerField()
    sent_orders = serializers.IntegerField()
    done_orders = serializers.IntegerField()

    shoe_orders = serializers.IntegerField()
    perfume_orders = serializers.IntegerField()

    sales_labels = serializers.ListField()
    sales_data = serializers.ListField()

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "username",
            "total_price",
            "payment_status",
            "status",
            "created_at",
            "items_count",
        ]

    def get_items_count(self, obj):
        return obj.items.count()

class ContactMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "username",
            "subject",
            "message",
            "status",
            "created_at",
        ]

class AdminTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminTask
        fields = "__all__"

class AdminLatestOrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "items_count",
            "total_price",
            "payment_status",
            "status",
            "created_at",
        ]

    def get_items_count(self, obj):
        return obj.items.count()

class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = "__all__"

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class WishlistSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "user",
            "username",
            "product",
            "product_title",
            "product_image",
            "created_at",
        ]
        read_only_fields = [
            "created_at"
        ]

class ContactMessageSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    message_type_display = serializers.CharField(
        source="get_message_type_display",
        read_only=True
    )

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "user",
            "username",
            "subject",
            "message_type",
            "message_type_display",
            "message",
            "status",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "created_at"
        ]


class NotificationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "username",
            "text",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "created_at"
        ]

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_superuser",
        ]