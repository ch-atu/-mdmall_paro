from django.urls import path, re_path
from order import views

urlpatterns = [
    path('order_temp/', views.OrderTempView.as_view()),
    path('order_forever/', views.OrderForeverView.as_view()),
    path('order_latest/', views.OrderLatestView.as_view()),
]



















