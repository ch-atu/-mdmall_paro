from django.urls import path, re_path
from django.conf.urls import include
from rest_framework import routers
from goods import views
from .views import MobileSearchView


router = routers.DefaultRouter()
router.register("", MobileSearchView, basename="mobile-search")
urlpatterns = [
    path('mobiles/', views.MobilesListView.as_view()),
    re_path(r'^detail/(?P<pk>\d+)/$', views.MobileComputerView.as_view()),
    path('computers/', views.ComputersListView.as_view()),

    re_path(r"api/search/", include(router.urls)),
]