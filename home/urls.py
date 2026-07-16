from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import dashboard
urlpatterns = [
    path("", views.home, name="home"),

    path("products/", views.products, name="products"),
    path("perfume/", views.perfume, name="perfume"),
    path("offers/", views.offers, name="offers"),

    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("tracking/", views.tracking, name="tracking"),
    path("terms/", views.terms, name="terms"),
    path("shipping/", views.shipping, name="shipping"),
    path('product/<str:slug>/', views.product_detail, name='product_detail'),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),
    path(
     "add-address/",
     views.add_address,
     name="add_address"
    ),
    # CART
    path("cart/", views.cart, name="cart"),
    path("cart/update/<int:id>/", views.update_cart, name="cart_update"),
    path(
     "order/<int:id>/",
     views.order_detail,
     name="order_detail"
    ),
    path(
     "add-to-cart/<int:id>/",
     views.add_to_cart,
     name="add_to_cart"
    ),
    path(
     "cart/remove/<int:id>/",
     views.remove_from_cart,
     name="remove_from_cart"
    ),
    path(
     "update-cart/<int:id>/",
     views.update_cart,
     name="update_cart"
    ),
    path("logout/", views.logout_view, name="logout"),
    path(
     'wishlist/add/<int:id>/',
     views.add_to_wishlist,
     name='add_to_wishlist'
    ),
    path('wishlist/toggle/<int:id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    path("wishlist/remove/<int:id>/", views.remove_from_wishlist),
    path("checkout/", views.checkout, name="checkout"),
    path("address/delete/<int:id>/", views.delete_address, name="delete_address"),
    path("address/edit/<int:id>/", views.edit_address, name="edit_address"),
    path(
     "change-password/",
     auth_views.PasswordChangeView.as_view(
        template_name="change_password.html"
     ),
     name="change_password"
    ),
    path(
    "password-done/",
     auth_views.PasswordChangeDoneView.as_view(
        template_name="password_done.html"
     ),
     name="password_done"
    ),
    path("notifications/", views.notifications, name="notifications"),
    path("api/notifications/", views.notifications_api, name="notifications_api"),
    path(
     "order/cancel/<int:id>/",
     views.cancel_order,
     name="cancel_order"
    ),
    path(
     "notification/read/<int:id>/",
     views.read_notification,
     name="read_notification"
    ),
    path('edit-email/', views.edit_email, name='edit_email'),
    path(
     "payment/<int:id>/",
     views.payment,
     name="payment"
    ),
    path("orders/<int:id>/status/<str:status>/", views.change_order_status, name="change_order_status"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("change-password/", views.change_password, name="change_password"),
    path("admin-panel/orders/", views.admin_orders, name="admin_orders"),
    path("admin-panel/orders/<int:id>/", views.admin_order_detail, name="admin_order_detail"),
    path("admin-panel/orders/<int:id>/edit/", views.admin_edit_order, name="admin_edit_order"),
    path("admin-panel/orders/<int:id>/delete/", views.admin_delete_order, name="admin_delete_order"),
    path(
     "admin-panel/products/",
     views.admin_products,
     name="admin_products"
    ),
    path(
     "admin-panel/products/add/",
     views.admin_add_product,
     name="admin_add_product"
    ),

    path(
     "admin-panel/products/<int:id>/edit/",
     views.admin_edit_product,
     name="admin_edit_product"
    ),

    path(
     "admin-panel/products/<int:id>/delete/",
     views.admin_delete_product,
     name="admin_delete_product"
    ),
    path("admin-panel/users/", views.admin_users, name="admin_users"),
    path("admin-panel/categories/", views.admin_categories, name="admin_categories"),
    path("admin-panel/wishlist/", views.admin_wishlist, name="admin_wishlist"),
    path(
     "admin-panel/wishlist/delete/<int:id>/",
     views.admin_delete_wishlist,
     name="admin_delete_wishlist",
    ),
    path("admin-panel/contacts/", views.admin_contacts, name="admin_contacts"),
    path(
     "admin-panel/contacts/delete/<int:id>/",
     views.admin_delete_contact,
     name="admin_delete_contact",
    ),
    path("admin-panel/notifications/", views.admin_notifications, name="admin_notifications"),
    path(
     "admin-panel/notifications/read/<int:id>/",
     views.admin_read_notification,
     name="admin_read_notification",
    ),

    path(
     "admin-panel/notifications/delete/<int:id>/",
     views.admin_delete_notification,
     name="admin_delete_notification",
    ),
    path("admin-panel/settings/", views.admin_settings, name="admin_settings"), 
    path("admin-panel/users/", views.admin_users, name="admin_users"),
    path("admin-panel/users/add/", views.admin_add_user, name="admin_add_user"),
    path("admin-panel/users/<int:id>/", views.admin_user_detail, name="admin_user_detail"),
    path("admin-panel/users/<int:id>/edit/", views.admin_edit_user, name="admin_edit_user"),
    path("admin-panel/users/<int:id>/delete/", views.admin_delete_user, name="admin_delete_user"),
    path(
     "admin-panel/categories/add/",
     views.add_category,
     name="add_category",
    ),

    path(
     "admin-panel/categories/edit/<int:id>/",
     views.edit_category,
     name="edit_category",
    ),

    path(
     "admin-panel/categories/delete/<int:id>/",
     views.delete_category,
     name="delete_category",
    ),
    path(
     "send-message/",
     views.send_message,
     name="send_message"
    ),
    path(
     "admin-panel/contacts/<int:id>/",
     views.admin_contact_detail,
     name="admin_contact_detail"
    ),
    path(
     "admin-panel/contacts/<int:id>/reply/",
     views.admin_reply_contact,
     name="admin_reply_contact",
    ),
    path(
     "my-tickets/",
     views.my_tickets,
     name="my_tickets",
    ),
    path(
     "my-tickets/<int:id>/",
     views.ticket_detail,
     name="ticket_detail",
    ),
    path(
     "my-tickets/<int:id>/close/",
     views.close_ticket,
     name="close_ticket",
    ),
    path(
     "admin-panel/notifications/read/<int:id>/",
     views.admin_read_notification,
     name="admin_read_notification"
    ),
    path(
     "admin-panel/contacts/read/<int:id>/",
     views.admin_read_contact,
     name="admin_read_contact"
    ),
]






