from django.urls import path
from store import views
urlpatterns = [
    path('', views.HomeView.as_view(),name="home"),
    path('product-detail', views.product_detail, name='product-detail'),
    path('cart', views.add_to_cart, name='add-to-cart'),
    path('buy', views.buy_now, name='buy-now'),
    path('profile', views.profile, name='profile'),
    path('address', views.address, name='address'),
    path('orders', views.orders, name='orders'),
    path('changepassword', views.change_password, name='changepassword'),
    path('mobile', views.mobile, name='mobile'),
]
