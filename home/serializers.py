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