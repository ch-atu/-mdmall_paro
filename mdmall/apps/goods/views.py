from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .serializers import Goods_MobilesSerializers, Goods_MobilesDetailSerializers, Goods_ComputerSerializers
from .models import MobileGoods, ComputerGoods
from rest_framework.response import Response
from rest_framework import status
from drf_haystack.viewsets import HaystackViewSet
from .serializers import GoodsSerializer

from utils.pagination import StandardResultsSetPagination


# Create your views here.

# class MobilesListView(APIView):
#     def get(self, request):
#         mobiles = MobileGoods.objects.all()
#         # for mobile in mobiles:
#         #     if mobile.specification_1:
#         #         mobile.run_memory = mobile.specification_1.run_memory
#         #         mobile.storage = mobile.specification_1.storage
#         #         mobile.color = mobile.specification_1.color
#         #     elif mobile.specification_2:
#         #         mobile.run_memory = mobile.specification_2.run_memory
#         #         mobile.storage = mobile.specification_2.storage
#         #         mobile.color = mobile.specification_2.color
#         #     elif mobile.specification_3:
#         #         mobile.run_memory = mobile.specification_3.run_memory
#         #         mobile.storage = mobile.specification_3.storage
#         #         mobile.color = mobile.specification_3.color
#
#         serialize = Goods_MobilesSerializers(instance=mobiles, many=True)
#         return Response(serialize.data, status=status.HTTP_200_OK)


class ComputersListView(ListAPIView):
    serializer_class = Goods_ComputerSerializers
    queryset = ComputerGoods.objects.all()


class MobilesListView(ListAPIView):
    serializer_class = Goods_MobilesSerializers
    queryset = MobileGoods.objects.all()


# class MobileView(RetrieveAPIView):
#     serializer_class = Goods_MobilesDetailSerializers
#     queryset = MobileGoods.objects.all()

# 详情
class MobileComputerView(APIView):
    def get(self, request, pk):
        if request.query_params['category'] == '电脑设备':
            computer_queryset = ComputerGoods.objects.filter(pk=pk)
            if not computer_queryset:
                data = {
                    'message': '查无此类别'
                }
                return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
            computer = computer_queryset[0]
            specifications = []
            if computer.specification_1:
                specifications.append({
                    'id': computer.specification_1.id,
                    'specification': computer.specification_1.size + '+' +
                                     computer.specification_1.run_memory + '+' +
                                     computer.specification_1.storage + '+' +
                                     computer.specification_1.color
                })
            if computer.specification_2:
                specifications.append({
                    'id': computer.specification_2.id,
                    'specification': computer.specification_2.size + '+' +
                                     computer.specification_2.run_memory + '+' +
                                     computer.specification_2.storage + '+' +
                                     computer.specification_2.color
                })
            if computer.specification_3:
                specifications.append({
                    'id': computer.specification_3.id,
                    'specification': computer.specification_3.size + '+' +
                                     computer.specification_3.run_memory + '+' +
                                     computer.specification_3.storage + '+' +
                                     computer.specification_3.color
                })
            computer = {
                'id': computer.id,
                'name': computer.name,
                # 'image': 'http://127.0.0.1:8000' + computer.image.url,
                'image': computer.image.url,
                'price': computer.price,
                'sales': computer.sales,
                'stock': computer.stock,
                'account': computer.account,
                'detail': computer.detail,
                'packing': computer.packing,
                'service': computer.service,
                'specifications': specifications,
                'category_id': computer.category.id
            }
            return Response(computer, status=status.HTTP_200_OK)
        if request.query_params['category'] == '手机通讯':
            mobile_queryset = MobileGoods.objects.filter(pk=pk)
            if not mobile_queryset:
                data = {
                    'message': '查无此类别'
                }
                return Response(data, status=status.HTTP_417_EXPECTATION_FAILED)
            mobile = mobile_queryset[0]
            specifications = []
            if mobile.specification_1:
                specifications.append({
                    'id': mobile.specification_1.id,
                    'specification': mobile.specification_1.run_memory + '+' +
                                     mobile.specification_1.storage + '+' +
                                     mobile.specification_1.color
                })
            if mobile.specification_2:
                specifications.append({
                    'id': mobile.specification_2.id,
                    'specification': mobile.specification_2.run_memory + '+' +
                                     mobile.specification_2.storage + '+' +
                                     mobile.specification_2.color
                })
            if mobile.specification_3:
                specifications.append({
                    'id': mobile.specification_3.id,
                    'specification': mobile.specification_3.run_memory + '+' +
                                     mobile.specification_3.storage + '+' +
                                     mobile.specification_3.color
                })
            mobile = {
                'id': mobile.id,
                'name': mobile.name,
                # 'image': 'http://127.0.0.1:8000' + mobile.image.url,
                'image': mobile.image.url,
                'price': mobile.price,
                'sales': mobile.sales,
                'stock': mobile.stock,
                'account': mobile.account,
                'detail': mobile.detail,
                'packing': mobile.packing,
                'service': mobile.service,
                'specifications': specifications,
                'category_id': mobile.category.id
            }
            return Response(mobile, status=status.HTTP_200_OK)


class MobileSearchView(HaystackViewSet):
    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    index_models = [MobileGoods, ComputerGoods]
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
