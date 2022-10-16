from django.urls import path, re_path
from cart import views

urlpatterns = [
    # 添加，查询购物车
    path('carts/', views.Cart.as_view()),
    # 购物车数量修改、选中状态修改、删除购物车中商品
    path('api/', views.CartApi.as_view()),
    # 查询购物车数量
    path('carts/count/', views.CartCountView.as_view())
]



















