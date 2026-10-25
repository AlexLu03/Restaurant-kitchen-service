from django.urls import path
from kitchen.views import (
    CookListView,
    DishListView,
    DishTypeListView,
)


urlpatterns = [
    path('cooks/', CookListView.as_view(), name='cook-list'),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishtypes/', DishTypeListView.as_view(), name='dishtype-list'),
]
