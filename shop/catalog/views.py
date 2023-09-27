from django.shortcuts import render
from catalog.models import Category, Product
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from catalog.serializers import CategorySerializer


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer
