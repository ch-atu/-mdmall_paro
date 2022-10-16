from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from alipay import AliPay
from order.models import Order
from payment.models import Payment


class PayView(APIView):
    def get(self, request):
        app_private_key_string = open('key/alipay/app_private_key.pem').read()
        alipay_public_key_string = open('key/alipay/alipay_public_key.pem').read()
        order_id = request.query_params.get('order_id')
        user_id = request.user.id
        # 查询是有有效订单
        try:
            order = Order.objects.get(order_id=order_id, user_id=user_id)
        except Exception as e:
            return Response({'message': '订单信息有误'}, status=status.HTTP_400_BAD_REQUEST)

        alipay = AliPay(
            appid='2021000116674090',
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2  加密方式推荐使用RSA2
            debug=True  # 默认False
        )
        # 调用SDK的方法得到支付链接后面的查询参数
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_id,  # 马上要支付的订单编号
            total_amount=order.price_count,  # 支付总金额, 它不认识Decimal 所以这里一定要转换类型
            subject='美多商城支付%s' % order.order_id,  # 标题
            return_url="http://localhost:8080/order_success/",  # 支付成功后的回调url
        )

        return Response({'alipay_url': 'https://openapi.alipaydev.com/gateway.do?' + order_string},
                        status=status.HTTP_200_OK)

    def put(self, request):
        data = request.query_params
        data = data.dict()
        signature = data.pop("sign")
        app_private_key_string = open('key/alipay/app_private_key.pem').read()
        alipay_public_key_string = open('key/alipay/alipay_public_key.pem').read()
        alipay = AliPay(
            appid='2021000116674090',
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2  加密方式推荐使用RSA2
            debug=True  # 默认False
        )
        # verification
        success = alipay.verify(data, signature)
        if success:
            if Payment.objects.filter(pay_id=data['trade_no']):
                return Response({'message': '重复提交', 'pay_id': data['trade_no']})
            else:
                order_id = data['out_trade_no']
                order = Order.objects.get(order_id=order_id, user_id=request.user.id)
                order.is_pay = True
                order.save()
                pay_id = data['trade_no']
                payment = Payment()
                payment.pay_id = pay_id
                payment.order_id = order.id
                payment.save()
                return Response({'message': 'ok', 'pay_id': data['trade_no']}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '修改支付结果失败'}, status=status.HTTP_304_NOT_MODIFIED)
