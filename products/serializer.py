from rest_framework import serializers
from .models import Product
from django.conf import settings

PRODUCT_ACTION_OPTIONS = settings.PRODUCT_ACTION_OPTIONS

class ProductActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()  #  "Like" -> "like"
        if not value in PRODUCT_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for products")
        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'content', 'image', 'price', 'media', 'likes']
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(data)< 4:
            raise serializers.ValidationError("This is not long enough")
        return data


class ProductSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'content', 'image', 'price', 'media', 'likes']
    def get_likes(self, obj):
        return obj.likes.count()

    def get_content(self, obj):
        return obj.content