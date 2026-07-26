from django.urls import path

from .api_views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductCreateAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    WishlistListAPIView,
    WishlistCreateAPIView,
    WishlistDeleteAPIView,
    WishlistToggleAPIView,
)
from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet
from .api_views import CartAPIView
from .api_views import CartItemCreateAPIView
from .api_views import CartItemUpdateAPIView
from .api_views import CartItemDeleteAPIView
from .api_views import ProfileAPIView
from .api_views import ProfileUpdateAPIView
from .api_views import OrderCreateAPIView
from .api_views import (
    AddressListCreateAPIView,
    AddressUpdateDeleteAPIView
)
from .api_views import OrderListAPIView
from .api_views import OrderDetailAPIView
from .api_views import (
    NotificationListAPIView,
    NotificationReadAPIView,
    TicketListAPIView,
    TicketCreateAPIView,
    TicketDetailAPIView,
    TicketReplyAPIView,
    TicketCloseAPIView,
)
from .api_views import CouponApplyAPIView



router = DefaultRouter()
router.register("products-viewset", ProductViewSet, basename="products")

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="api-products"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="api-product-detail"),
    path("products/create/", ProductCreateAPIView.as_view(), name="api-product-create"),
    path("products/<int:pk>/update/", ProductUpdateAPIView.as_view(), name="api-product-update",),
    path("products/<int:pk>/delete/", ProductDeleteAPIView.as_view(), name="api-product-delete"),
    path( "wishlist/", WishlistListAPIView.as_view(), name="api-wishlist"),
    path("wishlist/add/", WishlistCreateAPIView.as_view(), name="api-wishlist-add"),
    path("wishlist/<int:pk>/delete/", WishlistDeleteAPIView.as_view(), name="api-wishlist-delete"),
    path("wishlist/toggle/", WishlistToggleAPIView.as_view(), name="api-wishlist-toggle"),
    path("cart/", CartAPIView.as_view(), name="api-cart"),
    path("cart/add/", CartItemCreateAPIView.as_view(), name="api-cart-add"),
    path("cart/item/<int:pk>/update/", CartItemUpdateAPIView.as_view(), name="api-cart-item-update"),
    path("cart/item/<int:pk>/delete/", CartItemDeleteAPIView.as_view(), name="api-cart-item-delete"),
    path("profile/", ProfileAPIView.as_view(), name="api-profile"),
    path("profile/update/", ProfileUpdateAPIView.as_view(), name="api-profile-update"),
    path("orders/create/", OrderCreateAPIView.as_view(), name="api-order-create"),
    path("addresses/", AddressListCreateAPIView.as_view(), name="api-addresses"),
    path("addresses/<int:pk>/", AddressUpdateDeleteAPIView.as_view(), name="api-address-detail"),
    path("orders/", OrderListAPIView.as_view(), name="api-orders"),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="api-order-detail"),
    path("notifications/", NotificationListAPIView.as_view(), name="api-notifications"),
    path("notifications/<int:pk>/read/", NotificationReadAPIView.as_view(), name="api-notification-read"),
    path("tickets/", TicketListAPIView.as_view(), name="api-tickets"),
    path("tickets/create/", TicketCreateAPIView.as_view(), name="api-ticket-create"),
    path("tickets/<int:pk>/", TicketDetailAPIView.as_view(), name="api-ticket-detail"),
    path("tickets/<int:pk>/reply/", TicketReplyAPIView.as_view(), name="api-ticket-reply"),
    path("tickets/<int:pk>/close/", TicketCloseAPIView.as_view(), name="api-ticket-close"),
    path( "coupon/apply/", CouponApplyAPIView.as_view(), name="api-coupon-apply"),
]

urlpatterns += router.urls