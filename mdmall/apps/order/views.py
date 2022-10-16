from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .models import OrderTemp, Order, OrderInfo
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import time
import json
from utils.map_model import MAPGoods
from django.core.paginator import Paginator
from django_redis import get_redis_connection


class OrderTempView(APIView):
    """订单临时存储、查询"""

    def post(self, request):
        """新增多条订单临时存储数据"""
        OrderTemp.objects.filter(user_id=request.user.id).delete()
        order_temp_list = request.data['select_data']
        for i in order_temp_list:
            goods = MAPGoods[str(i['category_id'])].objects.get(id=i['goods_id'])
            i['user_id'] = request.user.id
            i['goods_price'] = goods.price
            i['total_price'] = goods.price * i['goods_count']
            i.pop('is_select')
            order = OrderTemp(**i)
            order.save()
        return Response('添加成功', status=status.HTTP_200_OK)

    def get(self, request):
        order_temp_queryset = OrderTemp.objects.filter(user_id=request.user.id)
        order_temp_list = []
        for order_temp in order_temp_queryset:
            goods = MAPGoods[str(order_temp.category_id)].objects.get(id=order_temp.goods_id)
            order_temp_info = {
                'goods_id': order_temp.goods_id,
                'goods_name': order_temp.goods_name,
                'goods_img': goods.image.url,
                'goods_count': order_temp.goods_count,
                'goods_price': order_temp.goods_price,
                'total_price': order_temp.total_price,
                'goods_status': order_temp.goods_status,
                'category_id': order_temp.category_id,
                'specification': order_temp.specification,
                'specification_id': order_temp.specification_id
            }
            order_temp_list.append(order_temp_info)
        return Response(order_temp_list, status=status.HTTP_200_OK)


class OrderForeverView(APIView):
    """订单存储、查询"""

    def post(self, request):
        # 添加订单
        add_order = {
            'home_id': request.data['home_id'],
            'pay_method': request.data['pay_method'],
            'user_id': request.user.id,
            'order_id': datetime.now().strftime('%Y%m%d%H%M%S') + str(time.time()).split('.')[1] + str(request.user.id),
        }
        order = Order(**add_order)
        order.save()
        order_price_list = []

        # 生成订单信息
        conn = get_redis_connection('cart')
        pl = conn.pipeline()
        goods_list = request.data['goods_list']
        for i in goods_list:
            goods = MAPGoods[str(i['category_id'])].objects.get(id=i['goods_id'])
            i['user_id'] = request.user.id
            i['order_id'] = order.id
            i['goods_price'] = goods.price
            i['total_price'] = goods.price * i['goods_count']
            order_price_list.append(i['total_price'])
            order_info = OrderInfo(**i)
            order_info.save()

            # 删除购物车已提交订单的数据
            pl.srem('set_%d' % request.user.id, i['goods_status'])
            pl.hdel('cart_%d' % request.user.id, i['goods_status'])
        # 添加订单的总价
        price_count = sum(order_price_list)
        order.price_count = price_count
        order.save()
        # 执行redis
        pl.execute()
        # 删除订单临时存储
        OrderTemp.objects.filter(user_id=request.user.id).delete()
        # 删除redis中的订单信息
        get_redis_connection('order').delete('order_%d' % request.user.id)
        return Response('添加订单成功', status=status.HTTP_200_OK)

    def get(self, request):
        conn = get_redis_connection('order')
        if not conn.get('order_%d' % request.user.id):
            user_id = request.user.id
            order_queryset = Order.objects.filter(user_id=user_id).order_by('-id')
            data = []
            for order in order_queryset:
                total_order_dict = {
                    'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'order_id': order.order_id,
                    'pay_method': order.pay_method,
                    'price_count': order.price_count,
                    'is_pay': order.is_pay
                }
                order_info_queryset = OrderInfo.objects.filter(order_id=order.id)
                order_info_list = []
                for order_info in order_info_queryset:
                    goods = MAPGoods[str(order_info.category_id)].objects.get(id=order_info.goods_id)
                    order_info_list.append({
                        'goods_id': order_info.goods_id,
                        'goods_name': order_info.goods_name,
                        'goods_img': goods.image.url,
                        'goods_count': order_info.goods_count,
                        'total_price': order_info.total_price,
                        'specification': order_info.specification
                    })
                total_order_dict['order_info_list'] = order_info_list
                data.append(total_order_dict)
            conn.set('order_%d' % request.user.id, json.dumps(data))
            p = Paginator(data, 5)
            result_data = p.page(1).object_list
            return Response({'order_data': result_data, 'count': len(data)}, status=status.HTTP_200_OK)

        else:
            data = conn.get('order_%d' % request.user.id)
            data = json.loads(data.decode())
            p = Paginator(data, 5)

            page = request.query_params.get('page')
            if not page:
                result_data = p.page(1).object_list
                return Response({'order_data': result_data, 'count': len(data)}, status=status.HTTP_200_OK)
            else:
                result_data = p.page(page).object_list
                return Response({'order_data': result_data, 'count': len(data)}, status=status.HTTP_200_OK)


class OrderLatestView(APIView):
    """获取最新的一条订单信息"""

    def get(self, request):
        user_id = request.user.id
        order_queryset = Order.objects.filter(user_id=user_id, is_pay=False).order_by('-id')
        if not order_queryset:
            return Response({'message': '没有订单信息', 'code': 0}, status=status.HTTP_200_OK)
        order_latest = order_queryset[0]
        order_id = order_latest.order_id
        order_price_count = order_latest.price_count
        return Response({'order_id': order_id, 'order_price_count': order_price_count}, status=status.HTTP_200_OK)