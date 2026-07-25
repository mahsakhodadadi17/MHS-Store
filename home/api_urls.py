from django.urls import path
from .api_views import ( ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView,ProductUpdateAPIView,ProductDeleteAPIView,)


urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="api-products"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="api-product-detail"),
    path("products/create/", ProductCreateAPIView.as_view(), name="api-product-create"),
    path("products/<int:pk>/update/", ProductUpdateAPIView.as_view(), name="api-product-update",),
    path("products/<int:pk>/delete/", ProductDeleteAPIView.as_view(), name="api-product-delete"),
]