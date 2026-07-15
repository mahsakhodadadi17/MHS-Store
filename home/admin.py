from django.contrib import admin
from django import forms

from .models import (
    Post,
    Category,
    Order,
    OrderItem
)



# ======================
# Product Admin
# ======================


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = "__all__"



class PostAdmin(admin.ModelAdmin):

    form = PostForm


    prepopulated_fields = {
        "slug": ("title",),
    }


    list_display = (
        "title",
        "price",
        "mojodi",
        "date",
    )



admin.site.register(Post, PostAdmin)



admin.site.register(Category)





# ======================
# Order Admin
# ======================



class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0





@admin.action(description="ارسال سفارش")

def make_sent(modeladmin, request, queryset):

    queryset.update(
        status="sent"
    )





@admin.action(description="تحویل سفارش")

def make_done(modeladmin, request, queryset):

    queryset.update(
        status="done"
    )





@admin.action(description="لغو سفارش")

def make_cancelled(modeladmin, request, queryset):

    queryset.update(
        status="cancelled"
    )







@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):


    list_display = (

        "id",

        "user",

        "payment_status",

        "status",

        "total_price",

        "created_at",

    )



    list_filter = (

        "status",

        "payment_status",

        "created_at",

    )



    search_fields = (

        "user__username",

        "user__email",

    )



    readonly_fields = (

        "created_at",

    )



    inlines = [

        OrderItemInline

    ]



    actions = [

        make_sent,

        make_done,

        make_cancelled,

    ]






@admin.register(OrderItem)

class OrderItemAdmin(admin.ModelAdmin):


    list_display = (

        "order",

        "product",

        "quantity",

        "price",

    )

from .models import ProductImage, ProductColor, ProductSize

admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(ProductSize)