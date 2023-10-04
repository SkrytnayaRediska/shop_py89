from rest_framework.serializers import ModelSerializer, Serializer
from catalog.models import Category, Product, Discount, Seller
from rest_framework import serializers
from datetime import date


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class DiscountSerializer(ModelSerializer):

    class Meta:
        model = Discount
        fields = ('id', 'percent', 'date_start', 'date_end', 'name')


class SellerSerializer(ModelSerializer):

    class Meta:
        model = Seller
        fields = ('id', 'name', 'country', 'description')


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()
    discount = DiscountSerializer()
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'articul', 'count_on_stock',
                  'discount', 'category', 'seller', 'description')


class AddProductSerializer(Serializer):
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()


class ProductInBasketSerializer(Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    discount_percent = serializers.IntegerField()


class BasketSerializer(Serializer):
    products = ProductInBasketSerializer(many=True)
    result_price = serializers.SerializerMethodField()

    def get_result_price(self, data):
        result_price = 0
        for item in data.get('products'):
            price = item.get('price')
            count = item.get('count')
            if item.get('discount'):
                percent = item.get('discount_percent')
                date_end = item.get('discount_date_end')
                delta = date.today() - date_end
                if delta.days <= 0:
                    result_price += (price * (100 - percent) / 100) * count
                else:
                    result_price += price * count
            else:
                result_price += price * count
        return result_price


class DeleteProductSerializer(Serializer):
    product_id = serializers.IntegerField()
