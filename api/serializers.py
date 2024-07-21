from rest_framework import serializers
from .models import FoodItem, Order

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all(), many=True)

    class Meta:
        model = Order
        fields = '__all__'
