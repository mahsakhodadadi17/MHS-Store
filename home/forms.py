from django import forms  
from django.forms import ModelForm
from .models import Contact
from .models import Post
 
class ContactForm(forms.ModelForm):
    class Meta:
        model  = Contact
        fields = ("__all__")




class ProductForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            "title",
            "content",
            "price",
            "discount",
            "mojodi",
            "image",
            "featured",
            "show_in_new",
            "category",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام محصول"
            }),

            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "discount": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "mojodi": forms.CheckboxInput(),

            "featured": forms.CheckboxInput(),

            "show_in_new": forms.CheckboxInput(),
        }





class ProductForm(forms.ModelForm):

    class Meta:

        model = Post

        fields = [
            "title",
            "category",
            "content",
            "price",
            "discount",
            "mojodi",
            "featured",
            "show_in_new",
            "image",
            "email",
            "date",
        ]