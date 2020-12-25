from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'content', 'image', 'price', 'media']

    def validate_content(self, value):
        if len(data)< 4:
            raise serializers.ValidationError("This is not long enough")
        return data