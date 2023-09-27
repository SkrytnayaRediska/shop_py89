from rest_framework.serializers import ModelSerializer
from catalog.models import Category, Product, Discount, Seller


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
