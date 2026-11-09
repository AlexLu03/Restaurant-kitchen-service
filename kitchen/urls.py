from django.urls import path
from kitchen.views import (
    CookListView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    CookDetailView,
    DishListView,
    DishTypeCreateView,
    DishTypeDeleteView,
    DishTypeListView,
    DishTypeUpdateView,
    DishCreateView,
    DishDeleteView,
    DishUpdateView,
    DishDetailView
)


urlpatterns = [
    path('cooks/', CookListView.as_view(), name='cook-list'),
    path('cooks/create/', CookCreateView.as_view(), name='cook-create'),
    path('cooks/<int:pk>/', CookDetailView.as_view(), name='cook-detail'),
    path(
        'cooks/<int:pk>/delete/', CookDeleteView.as_view(), name='cook-delete'
    ),
    path(
        'cooks/<int:pk>/update/', CookUpdateView.as_view(), name='cook-update'
    ),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishtypes/', DishTypeListView.as_view(), name='dishtype-list'),
    path(
        'dishtypes/create/',
        DishTypeCreateView.as_view(),
        name='dishtype-create'
    ),
    path(
        'dishtypes/<int:pk>/delete/',
        DishTypeDeleteView.as_view(),
        name='dishtype-delete'
    ),
    path(
        'dishtypes/<int:pk>/update/',
        DishTypeUpdateView.as_view(),
        name='dishtype-update'
    ),
    path(
        'dishes/create/',
        DishCreateView.as_view(),
        name='dish-create'
    ),
    path(
        'dishes/<int:pk>/delete/',
        DishDeleteView.as_view(),
        name='dish-delete'
    ),
    path(
        'dishes/<int:pk>/update/',
        DishUpdateView.as_view(),
        name='dish-update'
    ),
    path(
        'dishes/<int:pk>/',
        DishDetailView.as_view(),
        name='dish-detail'
    )
]

app_name = 'kitchen'
