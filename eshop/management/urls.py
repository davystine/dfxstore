from django.urls import path
from . import views

app_name = 'management'  # Namespace for this app

urlpatterns = [
    # Item URLs
    path('management/items/', views.ItemListView.as_view(), name='item_list'),
    path('management/items/add/', views.ItemCreateView.as_view(), name='item_add'),
    path('management/items/edit/<int:pk>/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('management/items/delete/<int:pk>/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # Category URLs
    path('management/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('management/categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('management/categories/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('management/categories/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
