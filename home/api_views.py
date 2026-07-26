from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Wishlist
from .serializers import WishlistSerializer
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer
from .serializers import CartItemSerializer
from .models import Profile
from .serializers import ProfileSerializer
from .serializers import OrderSerializer
from django.db import transaction
from .models import Address
from .serializers import AddressSerializer
from .models import Notification
from .serializers import NotificationSerializer
from .models import ContactMessage
from .models import TicketReply
from .serializers import TicketSerializer
from .serializers import TicketReplySerializer
from .models import Coupon
from .serializers import CouponApplySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "title",
        "content",
    ]

    filterset_fields = [
        "category",
        "price",
        "mojodi",
    ]

    ordering_fields = [
        "price",
        "date",
    ]

    ordering = [
        "-date",
    ]


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticated]

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer



class WishlistListAPIView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related("product")


class WishlistCreateAPIView(generics.CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product")

        try:
            product = Post.objects.get(id=product_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "محصول پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        if Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists():
            return Response(
                {"message": "این محصول قبلاً به علاقه‌مندی‌ها اضافه شده است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist = Wishlist.objects.create(
            user=request.user,
            product=product
        )

        serializer = WishlistSerializer(wishlist)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class WishlistDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            wishlist = Wishlist.objects.get(
                id=pk,
                user=request.user
            )
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "این محصول در علاقه‌مندی‌های شما وجود ندارد."},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist.delete()

        return Response(
            {"message": "محصول با موفقیت از علاقه‌مندی‌ها حذف شد."},
            status=status.HTTP_200_OK
        )


class WishlistToggleAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")

        try:
            product = Post.objects.get(id=product_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "محصول پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        if created:
            return Response(
                {"message": "به علاقه‌مندی‌ها اضافه شد."},
                status=status.HTTP_201_CREATED
            )

        wishlist_item.delete()

        return Response(
            {"message": "از علاقه‌مندی‌ها حذف شد."},
            status=status.HTTP_200_OK
        )

class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        return cart


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        product_id = request.data.get("product")
        color_id = request.data.get("color")
        size_id = request.data.get("size")
        quantity = request.data.get("quantity", 1)

        try:
            product = Post.objects.get(id=product_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "محصول پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            color_id=color_id,
            size_id=size_id,
            defaults={
                "quantity": quantity
            }
        )

        if not created:
            item.quantity += int(quantity)
            item.save()

        serializer = CartItemSerializer(item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class CartItemUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        )

class CartItemDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        )

class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )

        return profile

class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )

        return profile


class OrderCreateAPIView(generics.CreateAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    @transaction.atomic
    def create(self, request, *args, **kwargs):

        address_id = request.data.get("address")


        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        cart_items = CartItem.objects.filter(
            cart=cart
        )


        if not cart_items.exists():
            return Response(
                {
                    "error": "سبد خرید خالی است."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        total_price = sum(
            item.total_price
            for item in cart_items
        )


        order = Order.objects.create(
            user=request.user,
            address_id=address_id,
            total_price=total_price,
            final_price=total_price
        )


        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.item_price,
                color=item.color,
                size=item.size
            )


        cart_items.delete()


        serializer = OrderSerializer(order)


        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class AddressListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Address.objects.filter(
            user=self.request.user
        )


    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


class AddressUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Address.objects.filter(
            user=self.request.user
        )

class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items"
        )

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items"
        )

class NotificationListAPIView(generics.ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        print("USER =", self.request.user)
        print("AUTH =", self.request.auth)

        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


class NotificationReadAPIView(generics.UpdateAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        )


    def update(self, request, *args, **kwargs):

        notification = self.get_object()

        notification.is_read = True
        notification.save()

        serializer = NotificationSerializer(notification)

        return Response(serializer.data)


class TicketListAPIView(generics.ListAPIView):

    serializer_class = TicketSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return ContactMessage.objects.filter(
            user=self.request.user
        ).order_by("-created_at")



class TicketCreateAPIView(generics.CreateAPIView):

    serializer_class = TicketSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )



class TicketDetailAPIView(generics.RetrieveAPIView):

    serializer_class = TicketSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return ContactMessage.objects.filter(
            user=self.request.user
        )



class TicketReplyAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request, pk):

        try:

            ticket = ContactMessage.objects.get(
                id=pk,
                user=request.user
            )

        except ContactMessage.DoesNotExist:

            return Response(
                {
                    "detail": "تیکت پیدا نشد."
                },
                status=status.HTTP_404_NOT_FOUND
            )


        reply = TicketReply.objects.create(

            contact=ticket,

            user=request.user,

            message=request.data.get("message"),

            is_admin=False

        )


        serializer = TicketReplySerializer(reply)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )



class TicketCloseAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request, pk):

        try:

            ticket = ContactMessage.objects.get(
                id=pk,
                user=request.user
            )

        except ContactMessage.DoesNotExist:

            return Response(
                {
                    "detail": "تیکت پیدا نشد."
                },
                status=status.HTTP_404_NOT_FOUND
            )


        ticket.status = "closed"

        ticket.save()


        return Response(
            {
                "message": "تیکت بسته شد."
            }
        )


class CouponApplyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CouponApplySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        code = serializer.validated_data["code"]

        try:

            coupon = Coupon.objects.get(
                code=code
            )

        except Coupon.DoesNotExist:

            return Response(
                {
                    "detail": "کد تخفیف وجود ندارد."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not coupon.is_valid():

            return Response(
                {
                    "detail": "کد تخفیف معتبر نیست."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            order = Order.objects.filter(
                user=request.user,
                payment_status="unpaid"
            ).latest("created_at")

        except Order.DoesNotExist:

            return Response(
                {
                    "detail": "سفارش فعالی وجود ندارد."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if order.total_price < coupon.minimum_order:

            return Response(
                {
                    "detail": "حداقل مبلغ سفارش رعایت نشده است."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if coupon.discount_type == "percent":

            discount = (
                order.total_price * coupon.value
            ) // 100

            if coupon.max_discount:

                discount = min(
                    discount,
                    coupon.max_discount
                )

        else:

            discount = coupon.value

        order.coupon = coupon

        order.discount_amount = discount

        order.final_price = max(
            order.total_price - discount,
            0
        )

        order.save()

        coupon.used_count += 1

        coupon.save()

        return Response({

            "message": "کد تخفیف اعمال شد.",

            "discount": discount,

            "final_price": order.final_price

        })