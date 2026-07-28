from django.shortcuts import render , redirect
from .models import Post, Profile, Order , Cart
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from .models import Address
from .models import Order
from .models import CartItem
from django.http import JsonResponse
from .models import Wishlist
from .models import Cart, CartItem, Order, OrderItem
from .models import Notification
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.functions import TruncDate
import json
from django.views.decorators.http import require_POST
from .models import Contact
from .models import (
    Post,
    Cart,
    CartItem,
    Order,
    OrderItem,
    ProductColor,
    ProductSize,
)
from .forms import ProductForm, ColorFormSet, SizeFormSet, PerfumeFormSet
from .models import Banner
from django.contrib import messages
from .models import (Category,Wishlist, Contact, Notification,)
from .models import ContactMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ContactMessage
from .models import AdminNotification
from django.db.models.functions import TruncMonth
from datetime import timedelta
from django.utils import timezone
from .models import Profile
from .models import AdminTask
from .models import Discount , Coupon

def contact(request):
    form= ContactForm()
    return render(request, "form.html", {"form":form})




def home(request):

    shoes = Post.objects.filter(category__title='کفش')

    featured_posts = shoes.filter(
        featured=True
    ).order_by('order')

    latest_posts = shoes.filter(
        show_in_new=True
    ).order_by('order')[:5]

    slider_banners = Banner.objects.filter(
     banner_type="slider",
     section="shoes",
     active=True
    ).order_by("order")


    collection_banners = Banner.objects.filter(
     banner_type="collection",
     section="shoes",
     active=True
    ).order_by("order")

  


    return render(request, 'index.html', {

        'featured_posts': featured_posts,

        'latest_posts': latest_posts,

        'slider_banners': slider_banners,

        'collection_banners': collection_banners,

        'logo': 'image/main-logo.png',

        "logo_width": 170,

    })

from django.shortcuts import render, get_object_or_404



def perfume(request):
    perfumes = Post.objects.filter(category__title='عطر و ادکلن')
    featured_perfumes = perfumes.filter(featured=True).order_by('order')

    latest_perfumes = perfumes.filter(show_in_new=True).order_by('order')[:5]

    perfume_slider_banners = Banner.objects.filter(
     banner_type="slider",
     section="perfume",
     active=True
    ).order_by("order")


    perfume_collection_banners = Banner.objects.filter(
     banner_type="collection",
     section="perfume",
     active=True
    ).order_by("order")

    return render(request, 'perfume.html', {
         'featured_perfumes': featured_perfumes,
         'latest_perfumes': latest_perfumes,
         'logo': 'image/perfume-logo.png',
         "logo_width": 200,
         'perfume_slider_banners': perfume_slider_banners,
         'perfume_collection_banners': perfume_collection_banners,
    })

def about(request):
    return render(request, 'about.html')



def privacy(request):
    return render(request, 'privacy.html')

def tracking(request):
    return render(request, 'tracking.html')

def terms(request):
    return render(request, 'terms.html')

def shipping(request):
    return render(request, 'shipping.html')


def products(request):

    query = request.GET.get('q')

    products = Post.objects.all()


    if query:
        products = products.filter(
            title__icontains=query
        )


    return render(
        request,
        'products.html',
        {
            'products': products
        }
    )




def offers(request):

    now = timezone.now()


    discounts = Discount.objects.filter(
        active=True,
        start_date__lte=now,
        end_date__gte=now
    )


    return render(
        request,
        "offers.html",
        {
            "discounts": discounts
        }
    )
from django.shortcuts import render, get_object_or_404



    
def product_detail(request, slug):
    product = get_object_or_404(Post, slug=slug)

    images = product.images.all()
    colors = product.colors.all()
    sizes = product.sizes.all()
    perfume_detail = getattr(product, "perfume_detail", None)

    related_products = (
        Post.objects.filter(category=product.category)
        .exclude(id=product.id)
        .order_by("?")[:4]
    )

    return render(request, "product_detail.html", {
        "product": product,
        "images": images,
        "colors": colors,
        "sizes": sizes,
        "related_products": related_products,
        "perfume_detail": perfume_detail,
    })





from django.contrib.auth import authenticate, login


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")


        user = authenticate(
            username=username,
            password=password
        )


        if user:

            login(request,user)

            return redirect("dashboard")


        else:

            return render(
                request,
                "login.html",
                {
                    "error":"نام کاربری یا رمز عبور اشتباه است"
                }
            )


    return render(
        request,
        "login.html"
    )





def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)


        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("dashboard")


    else:

        form = UserCreationForm()


    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )

@login_required
def edit_profile(request):

    profile = request.user.profile


    if request.method == "POST":

        request.user.email = request.POST.get("email")

        profile.phone = request.POST.get("phone")


        if request.FILES.get("image"):

            profile.image = request.FILES.get("image")


        request.user.save()

        profile.save()


        return redirect("dashboard")


    return render(
        request,
        "edit_profile.html",
        {
            "profile": profile
        }
    )

@login_required
def dashboard(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")


    wishlist = Wishlist.objects.filter(
        user=request.user
    )


    addresses = Address.objects.filter(
        user=request.user
    )


    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")


    unread_count = notifications.filter(
        is_read=False
    ).count()



    completed_orders = orders.filter(
        status="done"
    ).count()


    pending_orders = orders.filter(
        status="pending"
    ).count()

    unread_notifications = Notification.objects.filter(
      user=request.user,
      is_read=False
    ).count()


    unread_tickets = ContactMessage.objects.filter(
     user=request.user,
     is_read=True
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "orders": orders,
            "wishlist": wishlist,
            "addresses": addresses,
            "notifications": notifications,
            "unread_count": unread_count,
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
            "unread_notifications": unread_notifications,
            "unread_tickets": unread_tickets,
        }
    )

@login_required
def add_address(request):

    if request.method == "POST":

        Address.objects.create(

            user=request.user,

            full_name=request.POST.get("full_name"),

            phone=request.POST.get("phone"),

            city=request.POST.get("city"),

            address=request.POST.get("address")

        )


        return redirect("dashboard")


    return render(
        request,
        "add_address.html"
    )

from django.shortcuts import get_object_or_404


@login_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )


    return render(
        request,
        "order_detail.html",
        {
            "order": order
        }
    )



from django.http import JsonResponse




@require_POST
@login_required
def update_cart(request, id):

    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    action = request.POST.get("action")
    quantity = request.POST.get("quantity")


    # دکمه + و -
    if action == "plus":
        item.quantity += 1

    elif action == "minus" and item.quantity > 1:
        item.quantity -= 1


    # تغییر مستقیم تعداد
    elif quantity:
        quantity = int(quantity)

        if quantity > 0:
            item.quantity = quantity


    item.save()


    cart = item.cart

    total = sum(
        i.product.price * i.quantity
        for i in cart.cartitem_set.all()
    )


    return JsonResponse({
        "status": "ok",
        "quantity": item.quantity,
        "total": total
    })
from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):

    logout(request)

    return redirect("/")

from .models import Wishlist


def add_to_wishlist(request, id):
    post = get_object_or_404(Post, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=post
    )

    return redirect('product_detail', slug=post.slug)


def toggle_wishlist(request, id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "login_required": True,
            "message": "ابتدا وارد حساب کاربری خود شوید"
        })

    post = get_object_or_404(Post, id=id)

    obj, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=post
    )

    if not created:
        obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({"liked": liked})



@login_required
def remove_from_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()

    return JsonResponse({"deleted": True})




@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = CartItem.objects.filter(
        cart=cart
    )

    total = 0

    for item in cart_items:
        total += item.total_price


    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(
        CartItem,
        id=id,
        cart__user=request.user
    )

    item.delete()

    return JsonResponse({"success": True})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem, Address


@login_required
def checkout(request):

    cart = get_object_or_404(Cart, user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect("cart")

    total = 0
    for item in cart_items:
        total += item.total_price

    coupon = None
    discount_amount = 0
    final_total = total

    if request.method == "POST":

        address_id = request.POST.get("address")

        address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user
        )

        coupon_code = request.POST.get("coupon")
        print("COUPON CODE:", coupon_code)

        if coupon_code:

            try:

                coupon = Coupon.objects.get(
                    code=coupon_code,
                    active=True
                )

                if coupon.is_valid() and total >= coupon.minimum_order:

                    if coupon.discount_type == "percent":

                        discount_amount = int(
                            total * coupon.value / 100
                        )

                        if coupon.max_discount:

                            discount_amount = min(
                                discount_amount,
                                coupon.max_discount
                            )

                    else:

                        discount_amount = coupon.value

                else:
                    coupon = None

            except Coupon.DoesNotExist:

                coupon = None

        final_total = total - discount_amount

        if final_total < 0:
            final_total = 0


        print("TOTAL:", total)
        print("DISCOUNT:", discount_amount)
        print("FINAL:", final_total)

        order = Order.objects.create(

            user=request.user,

            address=address,

            total_price=total,

            discount_amount=discount_amount,

            final_price=final_total,

            coupon=coupon,

            status="pending",

            payment_status="unpaid"

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

        if coupon:

            coupon.used_count += 1
            coupon.save()

        cart_items.delete()

        return redirect("payment", id=order.id)

    addresses = Address.objects.filter(user=request.user)

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
            "discount_amount": discount_amount,
            "final_total": final_total,
            "addresses": addresses,
        }
    )



def add_to_cart(request, id):

    # بررسی ورود کاربر
    if not request.user.is_authenticated:
        return JsonResponse({
            "added": False,
            "login_required": True,
            "message": "ابتدا وارد حساب کاربری خود شوید"
        })

    product = get_object_or_404(Post, id=id)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    color = None
    size = None

    color_id = request.POST.get("color")
    size_id = request.POST.get("size")

    if color_id:
        color = get_object_or_404(ProductColor, id=color_id)

    if size_id:
        size = get_object_or_404(ProductSize, id=size_id)

        # بررسی موجودی سایز
        if size.stock <= 0:
            return JsonResponse({
                "added": False,
                "message": "این سایز ناموجود است."
            })

    else:
        # اگر محصول سایز ندارد (مثل عطر)
        if product.stock <= 0:
            return JsonResponse({
                "added": False,
                "message": "این محصول ناموجود است."
            })

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        color=color,
        size=size,
        defaults={"quantity": 1},
    )

    if not created:

        if size:
            if item.quantity >= size.stock:
                return JsonResponse({
                    "added": False,
                    "message": "موجودی این سایز کافی نیست."
                })
        else:
            if item.quantity >= product.stock:
                return JsonResponse({
                    "added": False,
                    "message": "موجودی محصول کافی نیست."
                })

        item.quantity += 1
        item.save()

    return JsonResponse({
        "added": True,
        "quantity": item.quantity
    })

@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return redirect("dashboard")

@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)

    if request.method == "POST":
        address.full_name = request.POST.get("full_name")
        address.phone = request.POST.get("phone")
        address.city = request.POST.get("city")
        address.address = request.POST.get("address")
        address.save()
        return redirect("dashboard")

    return render(request, "edit_address.html", {"address": address})

@login_required
def notifications(request):
    return render(request, "notifications.html")

def notifications_api(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:10]

    data = []

    for n in notifications:
        data.append({
            "text": n.text,
            "is_read": n.is_read,
            "time": n.created_at.strftime("%H:%M")
        })

    return JsonResponse({"notifications": data})




@login_required
def read_notification(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user
    )

    notification.is_read = True
    notification.save()


    return redirect("dashboard")






@login_required
def cancel_order(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )


    if order.status in ["pending", "paid"]:

        order.status = "cancelled"

        order.save()


        Notification.objects.create(
            user=request.user,
            text=f"سفارش شماره {order.id} لغو شد"
        )


    return redirect("dashboard")




def change_password(request):
    return render(request, "change_password.html")


def edit_email(request):
    return render(request, "edit_email.html")


def delete_account(request):
    return render(request, "delete_account.html")

@login_required
def payment(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        # اگر قبلاً پرداخت شده
        if order.status == "paid":
            return redirect("order_detail", order.id)

        # ========= بررسی موجودی =========
        for item in order.items.all():

            # کفش
            if item.size:

                if item.size.stock < item.quantity:

                    messages.error(
                        request,
                        f"موجودی سایز {item.size.size} برای {item.product.title} کافی نیست."
                    )

                    return redirect("order_detail", order.id)

            # عطر
            else:

                if item.product.stock < item.quantity:

                    messages.error(
                        request,
                        f"موجودی {item.product.title} کافی نیست."
                    )

                    return redirect("order_detail", order.id)

        # ========= ثبت پرداخت =========
        order.status = "paid"
        order.payment_status = "paid"
        order.save()

        # ========= کم کردن موجودی =========
        for item in order.items.all():

            if item.size:

                item.size.stock -= item.quantity
                item.size.save()

            else:

                item.product.stock -= item.quantity
                item.product.save()

        Notification.objects.create(
            user=request.user,
            text=f"پرداخت سفارش شماره {order.id} با موفقیت انجام شد ✅"
        )

        messages.success(
            request,
            "پرداخت با موفقیت انجام شد."
        )

        return redirect("order_detail", order.id)

    return render(
        request,
        "payment.html",
        {
            "order": order,
            "total_price": order.total_price,
            "discount_amount": order.discount_amount,
            "final_price": order.final_price,
            "coupon": order.coupon,
        }
    )
from django.contrib.admin.views.decorators import staff_member_required



def admin_check(user):
    return user.is_staff



from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

ALLOWED_STATUSES = ["paid", "sent", "delivered", "cancelled"]

@staff_member_required
def change_order_status(request, id, status):

    if status not in ALLOWED_STATUSES:
        return redirect("admin_orders")

    order = get_object_or_404(Order, id=id)

    order.status = status
    order.save()

    Notification.objects.create(
        user=order.user,
        text=f"وضعیت سفارش شماره {order.id} تغییر کرد به {order.get_status_display()}"
    )

    return redirect("admin_orders")

from django.shortcuts import get_object_or_404, render






def admin_dashboard(request):

    total_orders = Order.objects.count()
    

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    paid_orders = Order.objects.filter(
        status="paid"
    ).count()

    sent_orders = Order.objects.filter(
        status="sent"
    ).count()

    done_orders = Order.objects.filter(
        status="done"
    ).count()

    notifications = AdminNotification.objects.filter(
     is_read=False
    ).order_by("-created_at")[:5]

    last30_labels = []
    last30_data = []

    for i in range(29, -1, -1):

        day = timezone.now().date() - timedelta(days=i)

        total = (
            Order.objects.filter(
              payment_status="paid",
             created_at__date=day
            ).aggregate(
               Sum("total_price")
            )["total_price__sum"] or 0
        )

        last30_labels.append(day.strftime("%d/%m"))
        last30_data.append(total)

        shoe_orders = OrderItem.objects.filter(
            product__category__title__icontains="کفش"
        ).aggregate(
           total=Count("id")
        )["total"] or 0


        perfume_orders = OrderItem.objects.filter(
            product__category__title__icontains="عطر"
        ).aggregate(
          total=Count("id")
        )["total"] or 0

        default_tasks = [

           "بررسی سفارش‌های جدید",

            "ارسال سفارش‌های پرداخت شده",

            "پاسخ به پیام‌های تماس با ما",

            "بررسی موجودی محصولات",

            "افزودن محصولات جدید",

          "بررسی گزارش فروش",
        ]

        for title in default_tasks:

            AdminTask.objects.get_or_create(

              title=title,

             is_default=True,

                defaults={

                 "created_by": request.user
                }
            )

        tasks = AdminTask.objects.order_by(
         "completed",
         "due_date",
         "-created_at"
        )





    context = {
        "products_count": Post.objects.count(),
        "notifications": notifications,
        "orders_count": total_orders,
        "users_count": User.objects.count(),

        "total_revenue": Order.objects.filter(
            payment_status="paid"
        ).aggregate(
            Sum("total_price")
        )["total_price__sum"] or 0,

        "pending_orders": pending_orders,
        "paid_orders": paid_orders,
        "sent_orders": sent_orders,
        "done_orders": done_orders,
        "recent_messages": ContactMessage.objects.select_related("user").order_by("-created_at")[:3],
        "latest_orders": Order.objects.select_related("user").prefetch_related("items").order_by("-created_at")[:10],
        "sales_labels": last30_labels,
        "sales_data": last30_data,
        "shoe_orders": shoe_orders,
        "perfume_orders": perfume_orders,
        "tasks": tasks,
    }


    return render(request, "admin_dashboard.html", context)

from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_orders(request):

    search = request.GET.get("search")


    latest_orders = (
        Order.objects
        .select_related("user")
        .prefetch_related("items")
        .all()
    )


    # 🔍 جستجو
    if search:

        latest_orders = latest_orders.filter(

            Q(id__icontains=search) |

            Q(user__username__icontains=search) |

            Q(user__email__icontains=search) |

            Q(tracking_code__icontains=search)
        )


    # مرتب سازی
    latest_orders = latest_orders.order_by("-created_at")



    return render(
        request,
        "admin_orders.html",
        {
            "latest_orders": latest_orders
        }
    )

@staff_member_required
def admin_order_detail(request, id):

    order = get_object_or_404(
        Order.objects.select_related(
            "user",
            "address"
        ).prefetch_related(
            "items__product"
        ),
        id=id
    )

    print("قبل:", order.admin_seen)

    if not order.admin_seen:
        order.admin_seen = True
        order.save(update_fields=["admin_seen"])

    order.refresh_from_db()

    print("بعد:", order.admin_seen)

    return render(
        request,
        "admin_order_detail.html",
        {
            "order": order
        }
    )


@staff_member_required
def admin_edit_order(request, id):

    order = get_object_or_404(Order, id=id)

    if request.method == "POST":

        order.status = request.POST.get("status")
        order.payment_status = request.POST.get("payment_status")

        order.save()

        messages.success(
            request,
            "سفارش با موفقیت بروزرسانی شد."
        )

        return redirect("admin_orders")

    return render(
        request,
        "admin_edit_order.html",
        {
            "order": order
        }
    )

@staff_member_required
def admin_delete_order(request, id):

    order = get_object_or_404(Order, id=id)

    order.delete()

    messages.success(
        request,
        "سفارش حذف شد."
    )

    return redirect("admin_orders")

@staff_member_required
def admin_products(request):

    products = Post.objects.select_related("category").order_by("-id")

    categories = Category.objects.all().order_by("title")

    return render(
        request,
        "admin_products.html",
        {
            "products": products,
            "categories": categories,
        }
    )

@staff_member_required
def admin_add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        colors = ColorFormSet(request.POST)
        sizes = SizeFormSet(request.POST)
        perfume = PerfumeFormSet(request.POST)


        if (
            form.is_valid()
            and colors.is_valid()
            and sizes.is_valid()
            and perfume.is_valid()
        ):

            product = form.save()


            colors.instance = product
            colors.save()


            sizes.instance = product
            sizes.save()


            perfume.instance = product
            perfume.save()


            return redirect("admin_products")


    else:

        form = ProductForm()

        colors = ColorFormSet()

        sizes = SizeFormSet()

        perfume = PerfumeFormSet()



    return render(
        request,
        "admin_add_product.html",
        {
            "form": form,
            "colors": colors,
            "sizes": sizes,
            "perfume": perfume,
        }
    )
@staff_member_required
def admin_edit_product(request, id):

    product = get_object_or_404(Post, id=id)

    if request.method == "POST":

        product.title = request.POST.get("title")
        product.price = request.POST.get("price")
        product.discount = request.POST.get("discount")
        product.content = request.POST.get("content")

        if request.FILES.get("image"):
            product.image = request.FILES["image"]

        # موجودی عطر
        if product.category.title == "عطر و ادکلن":
            product.stock = int(request.POST.get("stock", 0))

        product.save()

        # موجودی سایزهای کفش
        for size in product.sizes.all():

            stock = request.POST.get(f"stock_{size.id}")

            if stock is not None:
                size.stock = int(stock)
                size.save()

        return redirect("admin_products")

    return render(
        request,
        "admin_edit_product.html",
        {
            "product": product
        },
    )


@staff_member_required
def admin_delete_product(request, id):

    product = get_object_or_404(Post, id=id)

    product.delete()

    return redirect("admin_products")



@staff_member_required
def admin_delete_product(request, id):

    product = get_object_or_404(Post, id=id)

    product.delete()

    messages.success(request, "محصول با موفقیت حذف شد.")

    return redirect("admin_products")



@staff_member_required
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, "admin_categories.html", {"categories": categories})


@staff_member_required
def admin_wishlist(request):
    wishlist = Wishlist.objects.select_related("user", "product")
    return render(request, "admin_wishlist.html", {"wishlist": wishlist})


@staff_member_required
def admin_contacts(request):
    contacts = Contact.objects.all().order_by("-id")
    return render(request, "admin_contacts.html", {"contacts": contacts})


@staff_member_required
def admin_notifications(request):
    notifications = Notification.objects.all().order_by("-id")
    return render(
        request,
        "admin_notifications.html",
        {"notifications": notifications},
    )



from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_users(request):

    users = User.objects.all().order_by("-date_joined")

    q = request.GET.get("q")

    if q:
        users = users.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )

    role = request.GET.get("role")

    if role == "admin":
        users = users.filter(is_staff=True)

    elif role == "user":
        users = users.filter(is_staff=False)

    status = request.GET.get("status")

    if status == "active":
        users = users.filter(is_active=True)

    elif status == "inactive":
        users = users.filter(is_active=False)

    paginator = Paginator(users, 10)

    page = request.GET.get("page")

    users = paginator.get_page(page)

    context = {

        "users": users,

        "users_count": User.objects.count(),

        "active_users_count": User.objects.filter(is_active=True).count(),

        "inactive_users_count": User.objects.filter(is_active=False).count(),

        "admins_count": User.objects.filter(is_staff=True).count(),

    }

    return render(request, "admin_panel/admin_users.html", context)

@login_required
@user_passes_test(is_admin)
def admin_add_user(request):
    return render(request, "admin_panel/admin_add_user.html")


@login_required
@user_passes_test(is_admin)
def admin_user_detail(request, id):

    user_obj = get_object_or_404(
        User,
        id=id
    )

    orders = Order.objects.filter(
        user=user_obj
    )


    return render(
       request,
       "admin_panel/admin_user_detail.html",
       {
          "user_obj": user_obj,
           "orders": orders
        }
    )


@login_required
@user_passes_test(is_admin)
def admin_edit_user(request, id):

    user = get_object_or_404(User, id=id)

    return render(request, "admin_panel/admin_edit_user.html", {
        "user_detail": user
    })


@login_required
@user_passes_test(is_admin)
def admin_delete_user(request, id):

    user = get_object_or_404(User, id=id)

    user.delete()

    return redirect("admin_users")

from django.shortcuts import render, redirect, get_object_or_404
@staff_member_required
def add_category(request):
    if request.method == "POST":
        title = request.POST.get("title")

        if title:
            Category.objects.create(title=title)

    return redirect("admin_categories")

@staff_member_required
def edit_category(request, id):

    category = get_object_or_404(Category, id=id)

    if request.method == "POST":

        category.title = request.POST.get("title")
        category.save()

    return redirect("admin_categories")


@staff_member_required
def delete_category(request, id):

    category = get_object_or_404(Category, id=id)

    category.delete()

    return redirect("admin_categories")


@staff_member_required
def admin_wishlist(request):

    wishlists = Wishlist.objects.select_related(
        "user",
        "product"
    ).all()

    users_count = Wishlist.objects.values("user").distinct().count()

    return render(
        request,
        "admin_wishlist.html",
        {
            "wishlists": wishlists,
            "users_count": users_count,
        },
    )

@staff_member_required
def admin_delete_wishlist(request, id):

    wishlist = get_object_or_404(Wishlist, id=id)

    wishlist.delete()

    return redirect("admin_wishlist")


@staff_member_required
def admin_contacts(request):

    contacts = ContactMessage.objects.all().order_by("-created_at")

    today_messages = ContactMessage.objects.filter(
        created_at__date=timezone.now().date()
    ).count()

    return render(
        request,
        "admin_contacts.html",
        {
            "contacts": contacts,
            "today_messages": today_messages,
        }
    )
@staff_member_required
def admin_delete_contact(request, id):

    contact = get_object_or_404(Contact, id=id)

    contact.delete()

    return redirect("admin_contacts")

@staff_member_required
def admin_notifications(request):

    notifications = Notification.objects.select_related(
        "user"
    ).order_by("-created_at")


    unread_count = notifications.filter(
        is_read=False
    ).count()




    return render(
        request,
        "admin_notifications.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        },
    )

@staff_member_required
def admin_read_notification(request, id):

    notification = get_object_or_404(Notification, id=id)

    notification.is_read = True

    notification.save()

    return redirect("admin_notifications")

@staff_member_required
def admin_delete_notification(request, id):

    notification = get_object_or_404(Notification, id=id)

    notification.delete()

    return redirect("admin_notifications")

from django.shortcuts import render, redirect
from django.contrib import messages


from .models import SiteSettings


@login_required
def admin_settings(request):

    settings_data, created = SiteSettings.objects.get_or_create(id=1)

    if request.method == "POST":

        settings_data.site_name = request.POST.get("site_name")
        settings_data.admin_email = request.POST.get("admin_email")
        settings_data.phone = request.POST.get("phone")
        settings_data.address = request.POST.get("address")
        settings_data.instagram = request.POST.get("instagram")
        settings_data.telegram = request.POST.get("telegram")
        settings_data.about = request.POST.get("about")

        if request.FILES.get("shoe_logo"):
         settings_data.shoe_logo = request.FILES["shoe_logo"]

        if request.FILES.get("perfume_logo"):
         settings_data.perfume_logo = request.FILES["perfume_logo"]

        if request.FILES.get("favicon"):
          settings_data.favicon = request.FILES["favicon"]

        

        settings_data.maintenance = bool(request.POST.get("maintenance"))
        settings_data.registration = bool(request.POST.get("registration"))

        settings_data.save()

        messages.success(
            request,
            "تنظیمات با موفقیت ذخیره شد."
        )

        return redirect("admin_settings")

    return render(
        request,
        "admin_settings.html",
        {
            "site_name": settings_data.site_name,
            "admin_email": settings_data.admin_email,
            "phone": settings_data.phone,
            "address": settings_data.address,
            "instagram": settings_data.instagram,
            "telegram": settings_data.telegram,
            "about": settings_data.about,
            "maintenance": settings_data.maintenance,
            "registration": settings_data.registration,
            "shoe_logo": settings_data.shoe_logo,
            "perfume_logo": settings_data.perfume_logo,
            "favicon": settings_data.favicon,
            
        }
    )

def admin_user_detail(request, id):

    user_obj = get_object_or_404(
        User,
        id=id
    )

    return render(
        request,
        "admin_panel/admin_user_detail.html",
        {
            "user_obj": user_obj
        }
    )



from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ContactMessage


def tracking(request):

    order = None
    error = None

    if request.method == "POST":

        tracking_code = request.POST.get("tracking_code")

        try:

            order = Order.objects.get(
                tracking_code=tracking_code
            )

        except Order.DoesNotExist:

            error = "سفارشی با این کد رهگیری پیدا نشد."

    return render(
        request,
        "tracking.html",
        {
            "order": order,
            "error": error
        }
    )

from django.contrib import messages
 

@login_required
def send_message(request):

    if request.method == "POST":

        ContactMessage.objects.create(
            user=request.user,
            message_type=request.POST.get("message_type"),
            order_id=request.POST.get("order_id"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )

        AdminNotification.objects.create(

            title="پیام جدید پشتیبانی",

            message=f"{request.user.username} یک پیام جدید ارسال کرد"
        )

        messages.success(
            request,
            "پیام شما با موفقیت ارسال شد ✅"
        )
        print("MESSAGE SAVED")

        return redirect("tracking")


    return redirect("tracking")

@staff_member_required
def admin_delete_contact(request, id):
    contact = get_object_or_404(ContactMessage, id=id)
    contact.delete()
    return redirect("admin_contacts")

@staff_member_required
def admin_contact_detail(request, id):

    contact = get_object_or_404(ContactMessage, id=id)

    contact.is_read = True
    contact.save()

    return render(
        request,
        "admin_contact_detail.html",
        {
            "contact": contact
        }
    )

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from .models import ContactMessage, TicketReply

@staff_member_required
def admin_reply_contact(request, id):

    contact = get_object_or_404(ContactMessage, id=id)

    if request.method == "POST":

        TicketReply.objects.create(
            contact=contact,
            user=request.user,
            message=request.POST.get("message"),
            is_admin=True
        )

        contact.is_read = True
        contact.save()

        contact.status = "answered"
        contact.save()

    return redirect("admin_contact_detail", id=id)

@login_required
def my_tickets(request):

    tickets = ContactMessage.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_tickets.html",
        {
            "tickets": tickets
        }
    )

@login_required
def ticket_detail(request, id):

    ticket = get_object_or_404(
        ContactMessage,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        TicketReply.objects.create(
            contact=ticket,
            user=request.user,
            message=request.POST.get("message"),
            is_admin=False
        )

        return redirect("ticket_detail", id=id)

    return render(
        request,
        "ticket_detail.html",
        {
            "ticket": ticket
        }
    )

@login_required
def close_ticket(request, id):

    ticket = get_object_or_404(
        ContactMessage,
        id=id,
        user=request.user
    )

    ticket.status = "closed"
    ticket.save()

    return redirect(
        "ticket_detail",
        id=id
    )

@staff_member_required
def admin_notification_read(request, id):

    notification = get_object_or_404(
        Notification,
        id=id
    )

    notification.is_read = True
    notification.save()

    return redirect("admin_notifications")

@staff_member_required
def admin_read_contact(request, id):

    contact = get_object_or_404(
        ContactMessage,
        id=id
    )

    contact.is_read = True
    contact.save()

    return redirect("admin_contacts")

@login_required
def admin_managers(request):

    if not request.user.is_superuser:
        return redirect("admin_dashboard")

    managers = User.objects.filter(is_staff=True)

    return render(
        request,
        "admin_managers.html",
        {
            "managers": managers
        }
    )


@login_required
def admin_add_manager(request):

    if not request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
            return redirect("admin_add_manager")

        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً ثبت شده است.")
            return redirect("admin_add_manager")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_staff = True

        if role == "superadmin":
            user.is_superuser = True

        user.save()

        messages.success(request, "مدیر جدید با موفقیت ایجاد شد.")

        return redirect("admin_managers")

    return render(request, "admin_add_manager.html")


@login_required
def admin_edit_manager(request, id):

    if not request.user.is_superuser:
        return redirect("admin_dashboard")


    manager = get_object_or_404(
        User,
        id=id
    )


    profile, created = Profile.objects.get_or_create(
        user=manager
    )



    if request.method == "POST":


        manager.username = request.POST.get("username")

        manager.email = request.POST.get("email")


        role = request.POST.get("role")


        manager.is_staff = True

        manager.is_superuser = (
            role == "superadmin"
        )


        manager.save()



        profile_image = request.FILES.get(
            "profile_image"
        )


        if profile_image:

            profile.image = profile_image

            profile.save()



        messages.success(
            request,
            "اطلاعات مدیر با موفقیت ویرایش شد."
        )


        return redirect(
            "admin_managers"
        )



    return render(
        request,
        "admin_edit_manager.html",
        {
            "manager": manager
        }
    )
@login_required
def admin_delete_manager(request, id):

    if not request.user.is_superuser:
        return redirect("admin_dashboard")

    manager = get_object_or_404(User, id=id)

    # جلوگیری از حذف خودت
    if manager == request.user:
        messages.error(
            request,
            "شما نمی‌توانید حساب کاربری خودتان را حذف کنید."
        )
        return redirect("admin_managers")

    if request.method == "POST":
        manager.delete()

        messages.success(
            request,
            "مدیر با موفقیت حذف شد."
        )

        return redirect("admin_managers")

    return render(
        request,
        "admin_delete_manager.html",
        {
            "manager": manager
        }
    )


def admin_banners(request):

    banners = Banner.objects.all().order_by("order")

    return render(
        request,
        "admin_banners.html",
        {
            "banners": banners
        }
    )



def admin_add_banner(request):

    if request.method == "POST":

        banner = Banner.objects.create(

           title=request.POST.get("title"),

          banner_type=request.POST.get("banner_type"),
          section=request.POST.get("section"),
  
          layout=request.POST.get("layout"),

          link=request.POST.get("link"),

           order=request.POST.get("order") or 0,

          active=True if request.POST.get("active") else False,
        )


        if request.FILES.get("image"):

            banner.image = request.FILES.get("image")


        if request.FILES.get("video"):

            banner.video = request.FILES.get("video")

        if request.FILES.get("second_image"):

           banner.second_image = request.FILES.get("second_image")


        if request.FILES.get("second_video"):

          banner.second_video = request.FILES.get("second_video")


        banner.save()


        messages.success(
            request,
            "بنر با موفقیت اضافه شد"
        )


        return redirect("admin_banners")



    return render(
        request,
        "admin_add_banner.html"
    )


def admin_delete_banner(request, id):

    banner = get_object_or_404(
        Banner,
        id=id
    )

    banner.delete()

    messages.success(
        request,
        "بنر حذف شد"
    )

    return redirect("admin_banners")

def admin_edit_banner(request, id):

    banner = get_object_or_404(
        Banner,
        id=id
    )


    if request.method == "POST":

        banner.title = request.POST.get("title")
        banner.banner_type = request.POST.get("banner_type")
        banner.layout = request.POST.get("layout")
        banner.link = request.POST.get("link")
        banner.order = request.POST.get("order") or 0
        banner.active = True if request.POST.get("active") else False


        if request.FILES.get("image"):
            banner.image = request.FILES.get("image")


        if request.FILES.get("video"):
            banner.video = request.FILES.get("video")


        if request.FILES.get("second_image"):
            banner.second_image = request.FILES.get("second_image")


        if request.FILES.get("second_video"):
            banner.second_video = request.FILES.get("second_video")


        banner.save()


        messages.success(
            request,
            "بنر ویرایش شد"
        )


        return redirect("admin_banners")


    return render(
        request,
        "admin_edit_banner.html",
        {
            "banner": banner
        }
    )


def add_category(request):

    if request.method == "POST":

        title = request.POST.get("title")

        if title:
            Category.objects.create(
                title=title
            )

    return redirect("admin_categories")




@login_required
def toggle_admin_task(request, id):

    if not request.user.is_staff:
        return redirect("admin_dashboard")

    task = get_object_or_404(
        AdminTask,
        id=id
    )

    task.completed = not task.completed

    task.save()

    return redirect("admin_dashboard")

@login_required
def delete_admin_task(request, id):

    if not request.user.is_staff:
        return redirect("admin_dashboard")

    task = get_object_or_404(
        AdminTask,
        id=id
    )

    task.delete()

    messages.success(
        request,
        "کار حذف شد."
    )

    return redirect("admin_dashboard")

@login_required
def edit_admin_task(request, id):

    if not request.user.is_staff:
        return redirect("admin_dashboard")

    task = get_object_or_404(
        AdminTask,
        id=id
    )

    if request.method == "POST":

        task.title = request.POST.get("title")

        due_date = request.POST.get("due_date")

        task.due_date = due_date if due_date else None

        task.save()

        messages.success(
            request,
            "کار ویرایش شد."
        )

        return redirect("admin_dashboard")

    return render(
        request,
        "admin_edit_task.html",
        {
            "task": task
        }
    )

@login_required
def add_admin_task(request):

    if request.method == "POST":

        AdminTask.objects.create(

            title=request.POST.get("title"),

            due_date=request.POST.get("due_date") or None,

            created_by=request.user

        )

        messages.success(
            request,
            "کار جدید اضافه شد."
        )

    return redirect("admin_dashboard")

@login_required
def admin_discounts(request):

    if not request.user.is_staff:
        return redirect("admin_dashboard")


    discounts = Discount.objects.all().order_by("-created_at")


    for discount in discounts:

        now = timezone.now()

        if discount.start_date > now:

            discount.status = "pending"


        elif discount.end_date < now:

            discount.status = "expired"


        else:

            discount.status = "active"



    products = Post.objects.all()

    categories = Category.objects.all()



    return render(
        request,
        "admin_discounts.html",
        {
            "discounts": discounts,
            "products": products,
            "categories": categories,
        }
    )

@login_required
def add_discount(request):

    if not request.user.is_staff:
        return redirect("admin_dashboard")


    if request.method == "POST":

        discount = Discount.objects.create(

            title=request.POST.get("title"),

            discount_type=request.POST.get("discount_type"),

            value=request.POST.get("value"),

            start_date=request.POST.get("start_date"),

            end_date=request.POST.get("end_date"),

            active=True
        )


        # محصولات انتخاب شده
        product_ids = request.POST.getlist("products")

        if product_ids:
            discount.products.set(product_ids)


        # دسته‌بندی‌های انتخاب شده
        category_ids = request.POST.getlist("categories")

        if category_ids:
            discount.categories.set(category_ids)



        messages.success(
            request,
            "تخفیف با موفقیت اضافه شد."
        )


    return redirect("admin_discounts")

@login_required
def delete_discount(request, id):

    if not request.user.is_staff:
        return redirect("admin_dashboard")


    discount = get_object_or_404(
        Discount,
        id=id
    )

    discount.delete()


    messages.success(
        request,
        "تخفیف حذف شد."
    )


    return redirect("admin_discounts")

@login_required
def toggle_discount(request, id):

    if not request.user.is_staff:
        return redirect("admin_dashboard")


    discount = get_object_or_404(
        Discount,
        id=id
    )


    discount.active = not discount.active

    discount.save()


    messages.success(
        request,
        "وضعیت تخفیف تغییر کرد."
    )


    return redirect("admin_discounts")


@login_required
def admin_coupons(request):

    if not request.user.is_staff:
        return redirect("admin_dashboard")

    coupons = Coupon.objects.all().order_by("-id")

    return render(
        request,
        "admin_coupons.html",
        {
            "coupons": coupons
        }
    )


@login_required
def add_coupon(request):

    if not request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":

        Coupon.objects.create(

            code=request.POST.get("code"),

            discount_type=request.POST.get("discount_type"),

            value=request.POST.get("value"),

            minimum_order=request.POST.get("minimum_order"),

            usage_limit=request.POST.get("usage_limit"),

            start_date=request.POST.get("start_date"),

            end_date=request.POST.get("end_date"),

            active=True

        )

        messages.success(
            request,
            "کد تخفیف با موفقیت ساخته شد."
        )

    return redirect("admin_coupons")


from django.http import JsonResponse

@login_required
def apply_coupon(request):

    if request.method != "POST":
        return JsonResponse({"success": False})

    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price for item in cart_items)

    code = request.POST.get("coupon", "").strip()

    try:

        coupon = Coupon.objects.get(
            code=code,
            active=True
        )

    except Coupon.DoesNotExist:

        return JsonResponse({
            "success": False,
            "message": "کد تخفیف معتبر نیست."
        })

    if not coupon.is_valid():

        return JsonResponse({
            "success": False,
            "message": "این کد منقضی شده است."
        })

    if total < coupon.minimum_order:

        return JsonResponse({
            "success": False,
            "message": f"حداقل خرید {coupon.minimum_order:,} تومان است."
        })

    if coupon.discount_type == "percent":

        discount = int(total * coupon.value / 100)

        if coupon.max_discount:

            discount = min(discount, coupon.max_discount)

    else:

        discount = coupon.value

    final = max(total - discount, 0)

    return JsonResponse({

        "success": True,

        "discount": f"{discount:,}",

        "final": f"{final:,}"

    })


def admin_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            error = "نام کاربری یا رمز عبور اشتباه است."

    return render(request, "admin_login.html", {
        "error": error
    })