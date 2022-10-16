<template>
  <div>
    <my-header></my-header>
    <my-title-search :title="title"></my-title-search>

    <el-main style="background-color: white; margin: 0 8% 50px 8%; padding: 0">
      <div v-if="!is_pay">
        <el-card style="border-top: red solid 1px; background-color: #F7F7F7">
          <div style="display: flex">
            <i class="el-icon-circle-check" style="color: red;font-size: 88px"></i>
            <div class="order_info">
              <h4 style="margin: 0">订单提交成功，订单总价:<em style="font-size: 25px;color: red">￥{{ order_price_count }}</em></h4>
              <span style="font-size: 13px;margin-top: 10px">您的订单已经成功生成，订单号为: <em>{{ order_id }}</em></span>
              <el-button type="text" style="font-size: 13px" @click="$router.push('/user_center/user_order')">您可以在用户中心我的订单中查看详细情况</el-button>
            </div>
          </div>
        </el-card>
        <div class="ensure_pay">
          <el-button style="width: 150px;height: 50px;" type="danger" @click="goPay">确认支付</el-button>
        </div>
      </div>


      <el-card style="border-top: red solid 1px; background-color: #F7F7F7" v-if="is_pay">
        <div style="display: flex">
          <i class="el-icon-circle-check" style="color: red;font-size: 88px"></i>
          <div class="order_info">
            <h4 style="margin: 0">订单支付成功</h4>
            <span style="font-size: 13px;margin-top: 10px">您的订单已经成功支付，支付宝交易号为: <em>{{ pay_id }}</em></span>
            <el-button type="text" style="font-size: 13px" @click="$router.push('/user_center/user_order')">您可以在用户中心我的订单中查看详细情况</el-button>
          </div>
        </div>
      </el-card>
    </el-main>
    <my-footer></my-footer>

  </div>
</template>

<script>
import MyHeader from '@/components/my_header'
import MyFooter from '@/components/my_footer'
import MyTitleSearch from "@/components/my_title_search";
import {api_getOrderLatest} from "@/api/order.request";
import {api_getPayUrl} from "@/api/pay.request";
import {api_putPayment} from "@/api/pay.request";

export default {
  name: "order_success",
  components: {
    MyFooter,
    MyTitleSearch,
    MyHeader
  },
  created() {
    if(!Object.keys(this.$route.query).length){
      console.log('获取最近订单');
      this.getOrderLatest()
    }else {
      console.log('获取支付状态');
      this.putPayment()
    }
    console.log(this.$route, Object.keys(this.$route.query).length);
    console.log(this.$route, Object.keys(this.$route.query));
  },
  data(){
    return {
      order_id:'',
      order_price_count:'',
      is_pay:false,
      pay_id:'',
      title:'提交订单'
    }
  },
  methods: {
    getOrderLatest() {
      api_getOrderLatest().then(res => {
        console.log('获取最新订单信息', res);
        if(res.data.code===0){
          this.$router.push('/')
          this.$message({
            message:'您没有任何待支付的订单',
            type:"info",
            duration:1500
          })
        }
        this.order_id= res.data.order_id
        this.order_price_count= res.data.order_price_count
      }).catch(err => {
        console.log('获取最新订单信息错误', err);
      })
      console.log('获取订单');
    },
    putPayment(){
      const params = this.$route.query
      console.log('====',params, typeof params);
      api_putPayment(params).then(res=>{
        console.log('修改支付结果', res);
        this.pay_id = res.data.pay_id
        this.is_pay=true
        this.title='支付成功'
      }).catch(err=>{
        console.log('修改支付结果错误', err);
      })
    },
    goPay(){
      const order_id = this.order_id
      api_getPayUrl(order_id).then(res=>{
        console.log('获取支付接口', res);
        location.href = res.data.alipay_url
      }).catch(err=>{
        console.log('获取支付接口错误', err);
      })
    }
  }
}
</script>

<style scoped>
.order_info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 0 0 0 20px;
  justify-content: center
}

.ensure_pay {
  display: flex;
  justify-content: right;
  margin-top:20px;
}
</style>
