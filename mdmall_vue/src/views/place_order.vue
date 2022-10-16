<template>
  <div>
    <my-header></my-header>
    <my-title-search title="提交订单"></my-title-search>

    <el-main style="margin: 0 6%">
      <div class="ensure_home">
        <div class="place_order_title">
          <span>确认收货地址</span>
        </div>
        <el-card style="border-top: #D0312C solid 2px; background-color: #F7F7F7">
          <div style="display: flex;margin-bottom: 10px">
            <h5 style="margin: 0">寄送到:</h5>
          </div>
          <el-radio-group class="place_order_home" v-model="radio_home">
            <el-radio :label="user_home.id" v-for="user_home in user_homes" :key="user_home.id">
              <span>{{ user_home.area }}</span>&nbsp&nbsp&nbsp&nbsp
              <span>{{ user_home.address }}</span>
              （ <span>{{ user_home.receive }}</span> 收）
              <span>{{ user_home.mobile }}</span></el-radio>
          </el-radio-group>
        </el-card>
      </div>

      <div class="pay_method">
        <div class="place_order_title">
          <span>支付方式</span>
        </div>
      </div>
      <el-card style="border-top: #D0312C solid 2px; background-color: #F7F7F7">
        <el-radio-group class="place_order_pay" v-model="radio_pay">
          <el-radio :label="1" style="display: flex;align-items: center">
            <img src="@/assets/images/wechat.png" alt="">
          </el-radio>
          <el-radio :label="2" style="display: flex;align-items: center">
            <img src="@/assets/images/alipay.png" alt="">
          </el-radio>
        </el-radio-group>
      </el-card>

      <div class="goods_list">
        <div class="place_order_title">
          <span>商品列表</span>
        </div>
        <el-table
            ref="multipleTable"
            :data="tableData"
            tooltip-effect="dark"
            style="border-top: #D0312C solid 2px;">
          <el-table-column
              type="index"
              width="100%">
          </el-table-column>
          <el-table-column
              label="商品名称"
              show-overflow-tooltip>
            <template slot-scope="scope">
              <div style="display: flex;align-items: center;">
                <img style="width: 100px;height: 120px;margin-right: 10px" :src="scope.row.goods_img" alt="">
                <span>{{ scope.row.goods_name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column
              prop="specification"
              label="商品规格"
          width="220%">
          </el-table-column>
          <el-table-column
              label="商品价格"
              width="150%">
            <template slot-scope="scope">
              <span>{{scope.row.goods_price}} 元</span>
            </template>
          </el-table-column>
          <el-table-column
              prop="goods_count"
              label="数量"
              width="200%"
              show-overflow-tooltip>
          </el-table-column>
          <el-table-column
              label="小计"
              width="150%"
              show-overflow-tooltip>
            <template slot-scope="scope">
              <span>{{scope.row.total_price}} 元</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="total_settlement">
        <div class="place_order_title">
          <span>总金额结算</span>
        </div>

        <div class="total_settlement_down">
          <span>共 <i>{{tableData.length}}</i> 件商品，总金额: <i>{{ sum_price }}</i> 元 </span>
          <span>运费: <i>{{ freight.toFixed(2) }}</i> 元</span>
          <span>实付款: <i>{{ actual_sum_price }}</i> 元 </span>
        </div>
      </div>

      <div style="display: flex;justify-content: flex-end; margin-top: 20px">
        <el-button type="danger" @click="submitOrder" style="width: 130px;height: 50px">提交订单</el-button>
      </div>

    </el-main>

    <my-footer></my-footer>
  </div>
</template>

<script>
import MyFooter from '@/components/my_footer'
import MyHeader from '@/components/my_header'
import MyTitleSearch from '@/components/my_title_search'
import {api_getOrderTemp, api_addOrderForever} from "@/api/order.request";
import {getHome} from "@/api/user.request";


export default {
  name: "place_order",
  components: {
    MyFooter,
    MyHeader,
    MyTitleSearch
  },
  created() {
    this.getOrderTemp()
    this.getUserHome()
  },
  data() {
    return {
      radio_home: '',
      radio_pay: 1,
      tableData: [],
      freight:10.00,
      user_homes:[],
    }
  },
  computed:{
    sum_price(){
      let sum = 0
      for(let i of this.tableData){
        sum += i.total_price
      }
      return sum.toFixed(2)
    },
    actual_sum_price(){
      let result =parseFloat(this.sum_price)+this.freight
      return result.toFixed(2)
    }
  },
  methods:{
    getOrderTemp(){
      api_getOrderTemp().then(res=>{
        console.log('获取临时存储数据', res);
        this.tableData = res.data
      }).catch(err=>{
        console.log('获取临时存储数据失败', err);
      })
    },
    getUserHome(){
      getHome().then(res=>{
        console.log('获取用户的收货地址', res);
        this.user_homes = res.data
        for(let user_home of res.data){
          if(user_home.is_default){
            this.radio_home = user_home.id
          }
        }
      }).catch(err=>{
        console.log('获取用户收货地址错误', err);
      })
    },
    submitOrder(){
      if(this.tableData.length===0){
        this.$message('暂无可提交的订单')
      }else{
        const data = {
          home_id:this.radio_home,
          pay_method:this.radio_pay,
          goods_list:this.tableData
        }
        api_addOrderForever(data).then(res=>{
          console.log('提交订单并添加订单信息', res);
          this.$message({
            message:'提交订单成功',
            duration:1500,
            type:'success'
          })
          this.$router.push('/order_success')
        }).catch(err=>{
          console.log('提交订单并添加订单信息错误', err);
        })
      }
    }
  }
}
</script>

<style scoped>
@import '~@/css/main.css';

.place_order_title {
  display: flex;
  margin: 20px 0 10px 0
}

.place_order_home {
  display: flex;
  flex-direction: column;
  align-items: flex-start
}

.place_order_pay {
  display: flex;
}

.place_order_pay img {
  width: 135px;
  height: 75px;
  border: #ccc solid 1px
}

.total_settlement_down {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  border-top: #D0312C solid 2px;
  font-size: 12px;
  padding: 10px 0;
  background-color: #F7F7F7;
}

.total_settlement_down i {
  color: red;
  font-size: 20px;
}

.total_settlement_down span {
  margin-bottom: 5px;
  margin-right: 15px;
}

</style>
