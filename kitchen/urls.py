from django.urls import path
from kitchen.views import (
    CookListView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    DishListView,
    DishTypeListView,
)


urlpatterns = [
    path('cooks/', CookListView.as_view(), name='cook-list'),
    path('cooks/<int:pk>/', CookListView.as_view(), name='cook-detail'),
    path('cooks/create/', CookCreateView.as_view(), name='cook-create'),
    path('cooks/<int:pk>/delete/', CookDeleteView.as_view(), name='cook-delete'),
    path('cooks/<int:pk>/update/', CookUpdateView.as_view(), name='cook-update'),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishtypes/', DishTypeListView.as_view(), name='dishtype-list'),
]

app_name = 'kitchen'
