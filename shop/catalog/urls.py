from django.urls import path
from catalog.views import CategoriesListView, CategoryProductsView, \
    DiscountsListView, DiscountProductsView, SellersListView, SellerProductsView, \
    BasketView


urlpatterns = [
    path('categories/', CategoriesListView.as_view()),
    path('categories/<int:category_id>/', CategoryProductsView.as_view()),

    path('discounts/', DiscountsListView.as_view()),
    path('discounts/<int:discount_id>/', DiscountProductsView.as_view()),

    path('sellers/', SellersListView.as_view()),
    path('sellers/<int:seller_id>/', SellerProductsView.as_view()),

    path('basket/', BasketView.as_view())
]
