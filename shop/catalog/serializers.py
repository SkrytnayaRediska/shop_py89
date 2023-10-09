from rest_framework.serializers import ModelSerializer, Serializer
from catalog.models import Category, Product, Discount, Seller, Order, OrderProducts
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


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ('product', 'count')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductsSerializer(many=True, write_only=True)
    use_cashback = serializers.BooleanField(write_only=True)

    class Meta:
        model = Order
        fields = ('created_at', 'promocode', 'delivery_time',
                  'delivery_notif_in_time', 'delivery_method',
                  'delivery_address', 'delivery_status',
                  'payment_method', 'payment_statuses',
                  'result_price', 'products', 'use_cashback')
        read_only_fields = ('created_at', 'delivery_status',
                            'payment_statuses', 'result_price')

    def create(self, validated_data):
        products = validated_data.pop('products')
        use_cashback = validated_data.pop('use_cashback')
        promocode = validated_data.get('promocode')

        if promocode:
            delta_promocode = date.today() - promocode.date_end
            if delta_promocode.days > 0:
                promocode.percent = 0

        result_price = 0

        for record in products:
            product = record['product']
            count = record['count']
            if product.discount:
                percent = product.discount.percent
                date_end = product.discount.date_end
                delta = date.today() - date_end
                if delta.days <= 0:
                    result_price += (product.price * (100 - percent) / 100) * count
                else:
                    result_price += product.price * count
            else:
                result_price += product.price * count

        if promocode and promocode.is_cumulative:
            result_price = result_price * (100 - promocode.percent) / 100

        if use_cashback:
            if self.context['request'].user.cashback_points >= 100 and result_price >= 100:
                self.context['request'].user.cashback_points -= 100
                result_price -= 100
            elif self.context['request'].user.cashback_points >= result_price:
                self.context['request'].user.cashback_points -= result_price
                result_price = 0
            else:
                self.context['request'].user.cashback_points = 0
                result_price -= self.context['request'].user.cashback_points

            self.context['request'].user.save()


        order = Order.objects.create(result_price=result_price,
                                     user=self.context['request'].user,
                                     **validated_data)

        for product in products:
            OrderProducts.objects.create(order=order, **product)

        return order