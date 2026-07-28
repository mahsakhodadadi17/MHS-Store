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
from django.db.models import Sum
from .serializers import AdminDashboardSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from .serializers import ContactMessageSerializer
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from .models import AdminTask
from .serializers import AdminTaskSerializer
from .serializers import AdminLatestOrderSerializer
from .models import Discount
from .serializers import DiscountSerializer
from .serializers import CouponSerializer
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView)
from .models import Category
from .serializers import CategorySerializer
from .models import Wishlist
from .serializers import WishlistSerializer
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView
from .models import SiteSettings
from .serializers import SiteSettingsSerializer
from .models import Banner
from .serializers import BannerSerializer
from .serializers import ManagerSerializer




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

class AdminDashboardAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        data = {
            "orders_count": Order.objects.count(),
            "products_count": Post.objects.count(),
            "users_count": User.objects.count(),
            "total_revenue": Order.objects.filter(
                payment_status="paid"
            ).aggregate(
                total=Sum("total_price")
            )["total"] or 0,
        }

        return Response(data)


class AdminLatestOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest_orders = Order.objects.order_by("-created_at")[:10]

        serializer = OrderSerializer(latest_orders, many=True)

        return Response(serializer.data)

class AdminLatestOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        latest_orders = Order.objects.order_by("-created_at")[:10]

        serializer = OrderSerializer(latest_orders, many=True)

        return Response(serializer.data)

class AdminRecentMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = ContactMessage.objects.order_by("-created_at")[:10]

        serializer = ContactMessageSerializer(messages, many=True)

        return Response(serializer.data)

class AdminSalesChartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        start_date = timezone.now() - timedelta(days=30)

        sales = (
            Order.objects.filter(
                payment_status="paid",
                created_at__gte=start_date
            )
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(total=Sum("total_price"))
            .order_by("day")
        )

        labels = [
            item["day"].strftime("%Y-%m-%d")
            for item in sales
        ]

        data = [
            item["total"] or 0
            for item in sales
        ]

        return Response({
            "labels": labels,
            "data": data
        })

class AdminOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "pending_orders": Order.objects.filter(status="pending").count(),
            "paid_orders": Order.objects.filter(status="paid").count(),
            "sent_orders": Order.objects.filter(status="sent").count(),
            "done_orders": Order.objects.filter(status="done").count(),
        })

class AdminTaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AdminTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdminTask.objects.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class AdminTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminTask.objects.all()
    serializer_class = AdminTaskSerializer
    permission_classes = [IsAuthenticated]


class AdminLatestOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {"detail": "دسترسی ندارید."},
                status=403
            )

        latest_orders = (
            Order.objects
            .select_related("user")
            .prefetch_related("items")
            .order_by("-created_at")[:10]
        )

        serializer = AdminLatestOrderSerializer(
            latest_orders,
            many=True
        )

        return Response(serializer.data)

class AdminDiscountListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Discount.objects.all().order_by("-created_at")

class AdminDiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

class AdminCouponListCreateAPIView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all().order_by("-id")
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

class AdminCouponDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

class AdminUserListAPIView(generics.ListAPIView):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        users = User.objects.all().order_by("-date_joined")

        q = self.request.GET.get("q")

        if q:
            users = users.filter(
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q)
            )

        role = self.request.GET.get("role")

        if role == "admin":
            users = users.filter(is_staff=True)

        elif role == "user":
            users = users.filter(is_staff=False)

        status = self.request.GET.get("status")

        if status == "active":
            users = users.filter(is_active=True)

        elif status == "inactive":
            users = users.filter(is_active=False)

        return users

class AdminUserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class AdminUserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
class CategoryListCreateAPIView(ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AdminWishlistListAPIView(ListAPIView):

    queryset = Wishlist.objects.select_related(
        "user",
        "product"
    ).all()

    serializer_class = WishlistSerializer

    permission_classes = [IsAdminUser]



class AdminWishlistDetailAPIView(RetrieveDestroyAPIView):

    queryset = Wishlist.objects.select_related(
        "user",
        "product"
    ).all()

    serializer_class = WishlistSerializer

    permission_classes = [IsAdminUser]


class ContactMessageListAPIView(ListCreateAPIView):

    queryset = ContactMessage.objects.all().order_by("-created_at")

    serializer_class = ContactMessageSerializer



class ContactMessageDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ContactMessage.objects.all()

    serializer_class = ContactMessageSerializer


# لیست و ساخت اعلان‌ها (ادمین)
class NotificationListCreateAPIView(generics.ListCreateAPIView):

    queryset = Notification.objects.select_related(
        "user"
    ).all().order_by("-created_at")

    serializer_class = NotificationSerializer

    permission_classes = [IsAuthenticated]


# مشاهده، ویرایش، حذف یک اعلان
class NotificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Notification.objects.select_related(
        "user"
    ).all()

    serializer_class = NotificationSerializer

    permission_classes = [IsAuthenticated]


class AdminSiteSettingsAPIView(RetrieveUpdateAPIView):

    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):

        settings, created = SiteSettings.objects.get_or_create(id=1)

        return settings

class AdminBannerListCreateAPIView(ListCreateAPIView):

    queryset = Banner.objects.all().order_by("order")

    serializer_class = BannerSerializer

    permission_classes = [IsAdminUser]


class AdminBannerDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Banner.objects.all()

    serializer_class = BannerSerializer

    permission_classes = [IsAdminUser]


class AdminManagerListCreateAPIView(ListCreateAPIView):

    queryset = User.objects.filter(is_staff=True).order_by("id")

    serializer_class = ManagerSerializer

    permission_classes = [IsAdminUser]


class AdminManagerDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.filter(is_staff=True)

    serializer_class = ManagerSerializer

    permission_classes = [IsAdminUser]