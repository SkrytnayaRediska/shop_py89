from django.urls import path
from catalog.views import CategoriesListView


urlpatterns = [
    path('categories/', CategoriesListView.as_view()),
]
