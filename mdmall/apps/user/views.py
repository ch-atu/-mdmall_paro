from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from datetime import datetime
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer
from goods.models import Category

import mdmall.settings
from user.models import User, Home
from user.serializers import CreateUserSerializer, UserDetailSerializer, UserChangePassSerializer, UserHomeSerializers
from celery_tasks.send_email.tasks import send_verify_email
from utils.map_model import MAPGoods


# POST users/
class UserView(CreateAPIView):
    """创建用户"""
    serializer_class = CreateUserSerializer


# GET usernames/(?P<username>\w{5,20})/count/
class UsernameCountView(APIView):
    """判断用户是否已注册"""

    def get(self, request, username):
        # 查询user表
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            'username': username,
            'count': count
        }
        # 响应
        return Response(data)


# GET mobiles/(?P<mobile>1[3-9]\d{9})/count/
class UserMobileCountView(APIView):
    """判断手机号是否已注册"""

    def get(self, request, mobile):
        # 查询数据库
        count = User.objects.filter(mobile=mobile).count()
        # 构造响应数据
        data = {
            'mobile': mobile,
            'count': count
        }
        # 响应
        return Response(data)


# GET user/
class UserDetailView(RetrieveAPIView):
    """用户详细信息展示"""
    serializer_class = UserDetailSerializer

    # permission_classes = [IsAuthenticated]  # 指定权限,只有通过认证的用户才能访问当前视图

    def get_object(self):
        """重写此方法返回 要展示的用户模型对象"""
        return self.request.user


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# POST authorizations/
class UserAuthorizeView(ObtainJSONWebToken):
    """自定义账号密码登录视图,实现购物车登录合并"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUT change_pass/(?P<pk>\d+)/
class UserChangePass(UpdateAPIView):
    serializer_class = UserChangePassSerializer
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated, )


# POST/GET user_homes/
class UserHome(ListCreateAPIView):
    serializer_class = UserHomeSerializers

    def get_queryset(self):
        user_id = self.request.user.id
        homes = Home.objects.filter(user_id=user_id)
        return homes


# PUT/DELETE user_home/(?P<home_id>\d+)/
class UserChangeDeleteHome(APIView):
    def put(self, request, home_id):
        home = Home.objects.get(id=home_id)
        data = request.data
        if home.user_id != request.user.id:
            Response({'message': '查无此数据'})
        elif data.get('is_default') and len(data) == 1:
            default_home_queryset = Home.objects.filter(is_default=True)
            if not default_home_queryset:
                home.is_default = True
                home.save()
                return Response({'message': '设置默认成功', 'status': 1}, status=status.HTTP_200_OK)
            elif default_home_queryset[0] == home:
                return Response({'message': '已经是默认地址', 'status': 0})
            else:
                default_home_queryset[0].is_default = False
                default_home_queryset[0].save()
                home.is_default = True
                home.save()
                return Response({'message': '设置默认成功', 'status': 1}, status=status.HTTP_200_OK)
        else:
            home.receive = data['receive']
            home.area = data['area']
            home.address = data['address']
            home.mobile = data['mobile']
            home.email = data['email']
            home.save()
            return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    def delete(self, request, home_id):
        home = Home.objects.get(id=home_id)
        if home.user_id != request.user.id:
            return Response({'message': '查无此数据'})
        else:
            home.delete()
            return Response({'message': '删除成功'})


# POST/GET email/
class UserEmail(APIView):
    def get(self, request):
        token = request.query_params['token']
        try:
            serialize = TimedJSONWebSignatureSerializer(mdmall.settings.SECRET_KEY, expires_in=3600 * 24)
            data = serialize.loads(token)
        except:
            return Response('token已过期', status=status.HTTP_400_BAD_REQUEST)
        user_id = data['user_id']
        username = data['username']
        user = User.objects.filter(id=user_id, username=username)[0]
        if user:
            user.email_active = True
            user.save()
            return Response({'username': user.username, 'message': '激活成功'}, status=status.HTTP_200_OK)
        else:
            Response('激活失败', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        email = request.data['email']
        email_count = User.objects.filter(email=email).count()
        if email_count:
            return Response({'email': email, 'count': email_count}, status=status.HTTP_200_OK)
        user = request.user
        user.email = email
        user.save()
        return Response({'message': '邮箱添加成功', 'email': email}, status=status.HTTP_200_OK)

    def put(self, request):
        # 生成激活连接
        user_id = request.user.id
        username = request.user.username
        email = request.user.email
        serialize = TimedJSONWebSignatureSerializer(mdmall.settings.SECRET_KEY, expires_in=3600 * 24)
        token = serialize.dumps({'user_id': user_id, 'username': username}).decode()
        send_verify_email.delay(email, 'http://localhost:8080/active?token=%s' % token)
        return Response('send ok', status=status.HTTP_200_OK)


# POST/GET history/
class UserHistory(APIView):
    def post(self, request):
        if not request.user.id:
            return Response('no user', status=status.HTTP_200_OK)
        goods_id = request.data['good_id']
        category_id = request.data['category_id']
        try:
            if MAPGoods[category_id].objects.filter(id=goods_id):
                conn = get_redis_connection('history')
                pl = conn.pipeline()
                list_name = 'his_%d' % request.user.id
                list_goods = '%s-%s' % (goods_id, category_id)
                # 删除历史记录相同的值
                pl.lrem(list_name, 0, list_goods)
                # 向左添加一条历史记录
                pl.lpush(list_name, list_goods)
                pl.ltrim(list_name, 0, 4)
                pl.execute()
                return Response('添加历史记录成功', status=status.HTTP_200_OK)
            else:
                return Response('添加历史记录失败', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response('添加历史记录失败', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        conn = get_redis_connection('history')
        list_name = 'his_%d' % request.user.id
        his_list = conn.lrange(list_name, 0, -1)
        his_list_goods = []
        for i in his_list:
            goods_id, category_id = i.decode().split('-')
            goods = MAPGoods[category_id].objects.filter(id=goods_id)[0]
            category_name = Category.objects.get(id=category_id).name
            if goods.specification_1:
                specification_id = goods.specification_1.id
            elif goods.specification_2:
                specification_id = goods.specification_2.id
            else:
                specification_id = goods.specification_3.id
            his_list_goods.append({
                'goods_id': goods.id,
                'goods_name': goods.name,
                'goods_price': goods.price,
                # 'goods_img': 'http://127.0.0.1:8000' + goods.image.url,
                'goods_img': goods.image.url,
                'specifications_id': specification_id,
                'category_id': int(category_id),
                'category_name': category_name
            })
        return Response({'message': 'ok', 'his_goods_data': his_list_goods}, status=status.HTTP_200_OK)


class UserEmailCountView(APIView):
    def get(self, request, email):
        email_count = User.objects.filter(email=email).count()
        data = {
            'email': email,
            'count': email_count
        }
        return Response(data, status=status.HTTP_200_OK)
