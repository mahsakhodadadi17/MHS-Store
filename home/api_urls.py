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
    TicketListAPIView,
    TicketCreateAPIView,
    TicketDetailAPIView,
    TicketReplyAPIView,
    TicketCloseAPIView,
)
from .api_views import CouponApplyAPIView
from .api_views import AdminDashboardAPIView
from .api_views import AdminLatestOrdersAPIView
from .api_views import AdminRecentMessagesAPIView
from .api_views import AdminSalesChartAPIView
from .api_views import AdminOrderStatusAPIView
from .api_views import AdminTaskListCreateAPIView, AdminTaskDetailAPIView
from .api_views import AdminLatestOrdersAPIView
from .api_views import AdminDiscountListCreateAPIView, AdminDiscountDetailAPIView
from .api_views import (AdminCouponListCreateAPIView, AdminCouponDetailAPIView)
from .api_views import AdminUserListAPIView
from .api_views import AdminUserDetailAPIView
from .api_views import AdminUserCreateAPIView
from .api_views import ( CategoryListCreateAPIView, CategoryDetailAPIView)
from .api_views import ( AdminWishlistListAPIView, AdminWishlistDetailAPIView)
from .api_views import ( ContactMessageListAPIView, ContactMessageDetailAPIView)
from .api_views import ( NotificationListCreateAPIView, NotificationDetailAPIView)
from .api_views import ( NotificationListAPIView, NotificationReadAPIView,)
from .api_views import AdminSiteSettingsAPIView
from .api_views import ( AdminBannerListCreateAPIView, AdminBannerDetailAPIView)
from .api_views import ( AdminManagerListCreateAPIView, AdminManagerDetailAPIView)

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
    path( "my-notifications/", NotificationListAPIView.as_view(), name="my_notifications"),
    path( "my-notifications/<int:pk>/read/", NotificationReadAPIView.as_view(), name="read_notification"),
    path("tickets/", TicketListAPIView.as_view(), name="api-tickets"),
    path("tickets/create/", TicketCreateAPIView.as_view(), name="api-ticket-create"),
    path("tickets/<int:pk>/", TicketDetailAPIView.as_view(), name="api-ticket-detail"),
    path("tickets/<int:pk>/reply/", TicketReplyAPIView.as_view(), name="api-ticket-reply"),
    path("tickets/<int:pk>/close/", TicketCloseAPIView.as_view(), name="api-ticket-close"),
    path( "coupon/apply/", CouponApplyAPIView.as_view(), name="api-coupon-apply"),
    path("admin/dashboard/", AdminDashboardAPIView.as_view(), name="admin_dashboard_api"),
    path( "admin/recent-messages/", AdminRecentMessagesAPIView.as_view(), name="admin_recent_messages_api",),
    path( "admin/sales-chart/", AdminSalesChartAPIView.as_view(), name="admin_sales_chart_api",),
    path("admin/order-status/", AdminOrderStatusAPIView.as_view(), name="admin_order_status_api"),
    path("admin/tasks/", AdminTaskListCreateAPIView.as_view(), name="admin_tasks_api"),
    path("admin/tasks/<int:pk>/", AdminTaskDetailAPIView.as_view(), name="admin_task_detail_api"),
    path("admin/latest-orders/", AdminLatestOrdersAPIView.as_view(), name="admin_latest_orders_api"),
    path( "admin/discounts/", AdminDiscountListCreateAPIView.as_view(), name="admin_discounts_api"),
    path( "admin/discounts/<int:pk>/", AdminDiscountDetailAPIView.as_view(), name="admin_discount_detail_api"),
    path("admin/coupons/", AdminCouponListCreateAPIView.as_view(), name="admin_coupons_api"),
    path( "admin/coupons/<int:pk>/", AdminCouponDetailAPIView.as_view(), name="admin_coupon_detail_api"),
    path("admin/users/", AdminUserListAPIView.as_view(), name="admin_users_api"),
    path( "admin/users/<int:pk>/", AdminUserDetailAPIView.as_view(), name="admin_user_detail_api"),
    path( "admin/users/create/", AdminUserCreateAPIView.as_view(), name="admin_user_create_api"),
    path( "admin/categories/", CategoryListCreateAPIView.as_view(), name="admin_categories_api"),
    path( "admin/categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="admin_category_detail_api"),
    path( "admin/wishlists/", AdminWishlistListAPIView.as_view(), name="admin_wishlist_api"),
    path( "admin/wishlists/<int:pk>/", AdminWishlistDetailAPIView.as_view(), name="admin_wishlist_detail_api"),
    path( "contacts/", ContactMessageListAPIView.as_view(), name="contact_list_api"),
    path( "contacts/<int:pk>/", ContactMessageDetailAPIView.as_view(), name="contact_detail_api"),
    path( "admin/notifications/", NotificationListCreateAPIView.as_view(), name="notification_list_create_api"),
    path( "admin/notifications/<int:pk>/",  NotificationDetailAPIView.as_view(), name="notification_detail_api"),
    path( "admin/settings/", AdminSiteSettingsAPIView.as_view(), name="admin_settings_api"),
    path( "admin/banners/", AdminBannerListCreateAPIView.as_view(), name="admin_banners_api"),
    path( "admin/banners/<int:pk>/", AdminBannerDetailAPIView.as_view(), name="admin_banner_detail_api"),
    path( "admin/managers/", AdminManagerListCreateAPIView.as_view(), name="admin_managers_api"),
    path( "admin/managers/<int:pk>/", AdminManagerDetailAPIView.as_view(), name="admin_manager_detail_api"),
]

urlpatterns += router.urls