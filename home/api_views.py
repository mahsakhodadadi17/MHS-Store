from rest_framework import generics
from .models import Post
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = ProductSerializer