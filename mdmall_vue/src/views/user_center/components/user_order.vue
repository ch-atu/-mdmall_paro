<template>
  <div style="min-height: 500px">
    <div class="order_title">
      <span>全部订单</span>
    </div>

    <div v-if="order_list.length!==0">
      <div v-for="order in order_list">
        <el-card style=" margin-bottom: 20px;">
          <div class="order_info_title" style="display: flex;">
            <span style="margin:3px 100px 3px 30px">{{ order.create_time }}</span>
            <span style="margin: 3px 0">订单号: {{ order.order_id }}</span>
          </div>
          <div class="order_info" style="display: flex">
            <el-table
                :data="order.order_info_list"
                style="width: 100%"
                :show-header="false">
              <el-table-column
                  label="商品图片"
                  width="80px">
                <template slot-scope="scope">
                  <img style="width: 60px;height: 60px" :src="scope.row.goods_img" alt="">
                </template>
              </el-table-column>
              <el-table-column
                  prop="goods_name"
                  label="商品名称"
                  width="180px">
              </el-table-column>
              <el-table-column
                  prop="specification"
                  label="商品配置"
                  width="180px">
              </el-table-column>
              <el-table-column
                  prop="goods_count"
                  width="100px"
                  label="商品数量">
              </el-table-column>
              <el-table-column
                  prop="goods_price"
                  label="商品价格">
              </el-table-column>
            </el-table>
            <div>
              <span style="">{{ order.price_count }}元</span>
            </div>
            <div>
              <span>支付宝</span>
            </div>
            <div>
              <span v-if="order.is_pay">
                已付款
              </span>
              <button v-else>去付款</button>
            </div>
          </div>
        </el-card>
      </div>

      <el-pagination
          background
          layout="prev, pager, next, total,jumper"
          :page-size="5"
          :total="page_count"
          @current-change="changePage">
      </el-pagination>
    </div>

    <el-empty description="暂无订单信息" style="min-height: 399px" v-else></el-empty>

  </div>
</template>

<script>
import {api_getOrderForever} from "@/api/order.request";

export default {
  name: "user_order",
  created() {
    this.$store.commit('app/CHANGE_ACTIVE', 'user_order')
    this.getOrder()
  },
  data() {
    return {
      tableData: [],
      order_list: [],
      page_count: 0
    }
  },
  methods: {
    getOrder() {
      api_getOrderForever().then(res => {
        this.order_list = res.data.order_data
        this.page_count = res.data.count
        console.log('获取订单', res);
      }).catch(err => {
        console.log('获取订单失败', err);
      })
    },
    changePage(page){
      window.scrollTo(0,0)
      api_getOrderForever(page).then(res => {
        this.order_list = res.data.order_data
        this.page_count = res.data.count
        console.log('获取订单', res);
      }).catch(err => {
        console.log('获取订单失败', err);
      })
    }
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.order_info_title {
  border-top: #ECEEF4 solid 1px;
  border-left: #ECEEF4 solid 1px;
  border-right: #ECEEF4 solid 1px;
}

.order_info_title span {
  height: 23px;
  line-height: 23px;
  font-size: 15px;
}

.order_title {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 12px;
  font-size: 17px
}

.order_info div {
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: #ECEEF4 solid 1px;
  border-bottom: #ECEEF4 solid 1px;
  border-right: #ECEEF4 solid 1px;
  width: 120px;
}

.order_info span {
  /*margin: 0 50px*/
}

.el-table {
  border: #ECEEF4 solid 1px;
}
</style>
