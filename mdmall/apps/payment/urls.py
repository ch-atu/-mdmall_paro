from django.urls import path, re_path
from payment import views

urlpatterns = [
    path('payment/', views.PayView.as_view()),
]
