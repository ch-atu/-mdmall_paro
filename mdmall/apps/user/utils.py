import re
from django.core.exceptions import ValidationError


def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数,多追加 user_id和username"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'avatar': '用户头像路径',
        'mobile': user.mobile
    }


def validate_username(value):
    # pattern1 = r'[^\u4e00-\u9fa5]'
    # res1 = ''.join(re.findall(pattern1, value))
    # pattern2 = r'[a-zA-Z0-9_]*'
    # res2 = ''.join(re.findall(pattern2, res1))
    # if res2 != res1:
    #     raise ValidationError('用户名仅支持中英文、字母、数字、下划线')
    pattern = r'[^\u4e00-\u9fa5A-Za-z0-9_]*'
    res = ''.join(re.findall(pattern, value))
    if res:
        raise ValidationError('用户名仅支持中英文、字母、数字、下划线')




