from django.urls import path, re_path
from user import views

urlpatterns = [
    # 创建用户
    path('users/', views.UserView.as_view()),
    # 判断用户名是否已注册
    re_path(r'^usernames/(?P<username>.{3,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号是否已注册
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.UserMobileCountView.as_view()),

    # 获取用户详情
    re_path(r'^user/$', views.UserDetailView.as_view()),

    # jwt登录
    re_path(r'^authorizations/$', views.UserAuthorizeView.as_view()),  # 内部认证代码还是Django  登录成功生成token

    # 修改用户密码
    re_path(r'^change_pass/(?P<pk>\d+)/', views.UserChangePass.as_view()),

    # 用户收货地址
    path('user_homes/', views.UserHome.as_view()),

    # 用户修改、删除收货地址
    re_path(r'user_home/(?P<home_id>\d+)/', views.UserChangeDeleteHome.as_view()),

    # 发送激活邮箱,激活邮箱，添加邮箱
    path('email/', views.UserEmail.as_view()),

    # 用户历史浏览记录
    path('history/', views.UserHistory.as_view()),

    # 判断用户email是否已经被注册
    re_path(r'email/(?P<email>.*)/count/', views.UserEmailCountView.as_view())
]
