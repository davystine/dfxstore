from django.urls import path
from . import views

app_name ='store'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('accountinfo/', views.accountinfo, name='accountinfo'),
    path('account/', views.account, name='account'),
    path('password_update/', views.password_update, name='password_update'),
    path('item/<int:pk>', views.item, name='item'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path('search/', views.search, name='search'),
    path('rate/<int:pk>', views.rate_item, name='rate_item'),
]
