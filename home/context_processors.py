from .models import Notification, ContactMessage, Order
from .models import SiteSettings


def admin_notifications(request):

    if request.user.is_authenticated and request.user.is_staff:

        notifications_count = Notification.objects.filter(
            is_read=False
        ).count()


        contacts_count = ContactMessage.objects.filter(
            is_read=False
        ).count()

        orders_count = Order.objects.filter(
          admin_seen=False
        ).count()

    else:

        notifications_count = 0
        contacts_count = 0
        orders_count = 0


    return {
        "notifications_count": notifications_count,
        "contacts_count": contacts_count,
         "orders_count": orders_count,
    }


def site_settings(request):

    settings = SiteSettings.objects.first()

    return {
        "site_settings": settings
    }