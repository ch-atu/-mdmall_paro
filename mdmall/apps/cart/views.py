from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework import status
from goods.models import MobileGoods, ComputerGoods, MobileSpecification, ComputerSpecification


class Cart(APIView):
    def get(self, request):
        """查询购物车"""
        conn = get_redis_connection('cart')
        hash_name = 'cart_%d' % request.user.id
        carts_list_byte = conn.hkeys(hash_name)
        carts_list = []
        select_list = []
        price_together = 0
        for i in carts_list_byte:
            goods_status = i.decode()  # x-x-x

            goods_count = conn.hget(hash_name, goods_status).decode()  # 商品总数量
            is_select = conn.sismember('set_%d' % request.user.id, goods_status)  # 商品是否选中
            # 拆分x-x-x
            goods_content = goods_status.split('-')
            # 商品id
            goods_id = goods_content[0]
            # 类别id
            goods_category_id = goods_content[1]
            # 规格id
            goods_specification_id = goods_content[2]
            if goods_category_id == '1':
                mobile_goods = MobileGoods.objects.get(id=goods_id)
                specification = MobileSpecification.objects.get(id=goods_specification_id)
                goods = {
                    'goods_id': mobile_goods.id,
                    'goods_name': mobile_goods.name,
                    # 'goods_img': 'http://127.0.0.1:8000' + mobile_goods.image.url,
                    'goods_img': mobile_goods.image.url,
                    'goods_count': goods_count,
                    'goods_price': mobile_goods.price,
                    'total_price': int(goods_count) * float(mobile_goods.price),
                    'specification': f'{specification.run_memory}+{specification.storage}+{specification.color}',
                    'goods_status': goods_status,
                    'is_select': is_select,
                    'category_id': int(goods_category_id),
                    'specification_id': goods_specification_id,
                }
                carts_list.append(goods)
                if is_select:
                    select_list.append(goods)
            if goods_category_id == '2':
                computer_goods = ComputerGoods.objects.get(id=goods_id)
                specification = ComputerSpecification.objects.get(id=goods_specification_id)
                goods = {
                    'goods_id': computer_goods.id,
                    'goods_name': computer_goods.name,
                    # 'goods_img': 'http://127.0.0.1:8000' + computer_goods.image.url,
                    'goods_img': computer_goods.image.url,
                    'goods_count': goods_count,
                    'goods_price': computer_goods.price,
                    'total_price': int(goods_count) * float(computer_goods.price),
                    'specification': f'{specification.run_memory}+{specification.storage}+{specification.color}',
                    'goods_status': goods_status,
                    'is_select': is_select,
                    'category_id': int(goods_category_id),
                    'specification_id': goods_specification_id,
                }
                carts_list.append(goods)
                if is_select:
                    select_list.append(goods)

        for i in select_list:
            price_together += i['total_price']
        message = {
            'carts_list': carts_list,
            'price_together': price_together,
        }
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        """添加购物车"""
        conn = get_redis_connection('cart')
        pl = conn.pipeline()
        try:
            goods_id = request.data['goods_id']
            category_id = request.data['category_id']
            specification_id = request.data['specification_id']
            count = request.data['count']
        except Exception as e:
            return Response({'message': '请求出错'}, status=status.HTTP_400_BAD_REQUEST)
        hash_name = 'cart_' + str(request.user.id)
        # goods_id-category_id-specification_id
        cart_goods = '%d-%d-%d' % (goods_id, category_id, specification_id)
        pl.hincrby(hash_name, cart_goods, count)
        pl.execute()
        return Response({'message': '添加购物车成功'}, status=status.HTTP_200_OK)


class CartApi(APIView):
    def put(self, request):
        """购物车数量的改变，全选，全不选、单选"""
        conn = get_redis_connection('cart')
        if request.data['opt'] == 'change_count':
            hash_name = 'cart_%d' % request.user.id
            goods_status = request.data['goods_status']
            count = request.data['count']
            conn.hset(hash_name, goods_status, count)
            return Response('修改数量成功', status=status.HTTP_200_OK)
        if request.data['opt'] == 'select':
            set_name = 'set_%d' % request.user.id
            if isinstance(request.data['val'], dict):
                # 单选/不选
                goods_status = request.data['val']['goods_status']
                if conn.sismember(set_name, goods_status):
                    conn.srem(set_name, goods_status)
                else:
                    conn.sadd(set_name, goods_status)
                return Response('success', status=status.HTTP_200_OK)
            if isinstance(request.data['val'], list) and request.data['val']:
                # 全选
                pl = conn.pipeline()
                for i in request.data['val']:
                    pl.sadd(set_name, i['goods_status'])
                pl.execute()
                return Response('全选', status=status.HTTP_200_OK)
            if isinstance(request.data['val'], list) and not request.data['val']:
                # 全不选
                conn.delete(set_name)
                return Response('全不选', status=status.HTTP_200_OK)

        return Response('错误的请求', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """删除购物车某一条数据"""
        conn = get_redis_connection('cart')
        pl = conn.pipeline()
        goods_status = request.data['goods_status']
        pl.srem('set_%d' % request.user.id, goods_status)
        pl.hdel('cart_%d' % request.user.id, goods_status)
        pl.execute()
        return Response('删除成功', status=status.HTTP_200_OK)


class CartCountView(APIView):
    def get(self, request):
        if not request.user.id:
            return Response({'count': 0}, status=status.HTTP_200_OK)
        conn = get_redis_connection('cart')
        hash_name = 'cart_%d' % request.user.id
        carts_list_byte = conn.hkeys(hash_name)
        count = len(carts_list_byte)
        return Response({'count': count}, status=status.HTTP_200_OK)
