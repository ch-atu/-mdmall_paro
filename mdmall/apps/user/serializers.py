from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

from user.models import User, Home
import re


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    # 序列化器的所有字段: ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 需要校验的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 模型中已存在的字段: ['id', 'username', 'password', 'mobile']

    # 需要序列化的字段: ['id', 'username', 'mobile', 'token']
    # 需要反序列化的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    password2 = serializers.CharField(label='确认密码', write_only=True)
    token = serializers.CharField(label='token', read_only=True)
    code = serializers.CharField(label='验证码', write_only=True)

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        # fields = '__all__'
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'token', 'code']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 3,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许3-20个字符的用户名',
                    'max_length': '仅允许3-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            },
        }

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式有误')
        return value

    def validate(self, attrs):
        """校验密码两个是否相同"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        # # 校验验证码
        # redis_conn = get_redis_connection('verify_codes')
        # mobile = attrs['mobile']
        # real_sms_code = redis_conn.get('sms_%s' % mobile)
        # # 向redis存储数据时都是以字条串进行存储的,取出来后都是bytes类型 [bytes]
        #
        # if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
        #     raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        # 把不需要存储的 password2, sms_code, allow 从字段中移除
        del validated_data['password2']
        del validated_data['code']
        # 把密码先取出来
        password = validated_data.pop('password')
        # 创建用户模型对象, 给模型中的 username和mobile属性赋值

        user = User(**validated_data)

        user.set_password(password)  # 把密码加密后再赋值给user的password属性
        user.save()  # 存储到数据库

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的叫jwt_payload_handler函数(生成payload)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt

        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成完整的jwt

        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']


class UserChangePassSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(label='新密码', write_only=True)
    new_password2 = serializers.CharField(label='确认密码', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'new_password', 'new_password2']
        extra_kwargs = {  # 修改字段选项
            'password': {
                'write_only': True,
            },
            'id': {
                'read_only': True,
            },
            'username': {
                'read_only': True,
            },
        }

    def validate(self, attrs):
        username = self.context['request'].user.username
        password = attrs['password']
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError('两次密码不一致')
        if len(attrs['new_password']) < 8:
            raise serializers.ValidationError('密码的长度小于8位数')
        user = authenticate(username=username, password=password)
        if user:
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('当前密码错误')

    def update(self, instance, validated_data):
        del validated_data['password']
        del validated_data['new_password2']
        new_password = validated_data.pop('new_password')
        instance = validated_data.pop('user')
        instance.set_password(new_password)
        instance.save()
        return instance


class UserHomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        validated_data['user_id'] = user_id
        home = Home(**validated_data)
        home.save()
        return home












