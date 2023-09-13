from django.urls import path, include
from users.views import ActivateUser, SomeView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('accounts/activate/<uid>/<token>/',
         ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('some-view/', SomeView.as_view())
]