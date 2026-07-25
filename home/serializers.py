from rest_framework import serializers
from .models import Post


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "قیمت نمی‌تواند منفی باشد."
            )
        return value