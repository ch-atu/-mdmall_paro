<template>
  <div>
    <my-header></my-header>
    <my-title-search title="购物车"></my-title-search>


    <el-main style="margin: 0 6%" v-cloak>
      <div style="display: flex; margin-bottom: 15px">
        <span>全部商品<em style="color: red"> {{ tableData.length }} </em>件</span>
      </div>

      <div class="cart_info">
        <el-table
            ref="multipleTable"
            :data="tableData"
            tooltip-effect="dark"
            style="width: 100%">
          <el-table-column
              width="100%">
            <template slot="header" slot-scope="scope">
              <input type="checkbox" :checked="check_all" @click="handleAllSelection">
            </template>
            <template slot-scope="scope">
              <input type="checkbox" :checked="scope.row.is_select" @click="handleSingleSelection(scope.row)">
            </template>
          </el-table-column>
          <el-table-column
              label="商品名称"
              width="300%"
              show-overflow-tooltip>
            <template slot-scope="scope">
              <div style="display: flex;align-items: center">
                <img style="width: 100px;height: 120px;" :src="scope.row.goods_img" alt="">
                <span>{{ scope.row.goods_name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column
              prop="specification"
              label="商品规格"
              width="150%">
          </el-table-column>
          <el-table-column
              prop="goods_price"
              label="商品价格"
              width="150%">
          </el-table-column>
          <el-table-column
              prop="goods_count"
              label="数量"
              width="200%"
              show-overflow-tooltip>
            <template slot-scope="scope">
              <el-input-number v-model="scope.row.goods_count" @change="changeCount(scope.row.goods_status, $event)"
                               :min="1" size="small">
              </el-input-number>
            </template>
          </el-table-column>
          <el-table-column
              prop="total_price"
              label="小计"
              width="150%"
              show-overflow-tooltip>
          </el-table-column>
          <el-table-column
              prop="option"
              label="操作"
              show-overflow-tooltip>
            <template slot-scope="scope">
              <el-button type="text" @click="deleteCart(scope.row.goods_status)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="cart_info_down">
          <div style="margin-right: 20px">
            <div style="margin-bottom: 10px">
              <span>合计(不含运费):
                <span style="color: red">￥</span>
                <span style="color: red;font-size: 25px">{{ price_together }}</span>
              </span>
            </div>

            <div style="display: flex;justify-content: flex-end">
              <div>
                <span>共计<span style="color: red"> {{ select_data.length }} </span>件商品</span>
              </div>
            </div>
          </div>
          <div>
            <el-button type="danger" @click="goPay" style="width: 120px; height: 80px">
              <span style="font-size: 20px">去结算</span>
            </el-button>
          </div>
        </div>
      </div>
    </el-main>

    <my-footer></my-footer>
  </div>
</template>

<script>
import MyHeader from '@/components/my_header'
import MyFooter from '@/components/my_footer'
import MyTitleSearch from '@/components/my_title_search'
import {api_getCart, api_updateCart, api_deleteCart} from "@/api/cart.request";
import {api_addOrderTemp} from "@/api/order.request";

export default {
  name: "cart",
  components: {
    MyHeader,
    MyFooter,
    MyTitleSearch
  },
  created() {
    this.getCarts()
  },
  data() {
    return {
      tableData: [],
      price_together: '',
      select_data: [],
    }
  },
  computed: {
    check_all() {
      if (this.select_data.length === 0) {
        return false
      } else {
        return this.select_data.length === this.tableData.length
      }
    }
  },
  methods: {
    handleAllSelection() {
      console.log('勾选回调');
      let data = {}
      if (this.select_data.length !== this.tableData.length) {
        data = {
          val: this.tableData,
          opt: 'select'
        }
      } else {
        data = {
          val: [],
          opt: 'select'
        }
      }
      api_updateCart(data).then(res => {
        console.log('处理勾选状态', res);
        this.select_data = []
        this.getCarts()
      }).catch(err => {
        console.log('处理勾选状态错误', err);
      })
    },
    handleSingleSelection(row) {
      console.log(row);
      const data = {
        val: row,
        opt: 'select'
      }
      api_updateCart(data).then(res => {
        console.log('处理勾选状态', res);
        this.select_data = []
        this.getCarts()
      }).catch(err => {
        console.log('处理勾选状态错误', err);
      })
    },
    changeCount(goods_status, val) {
      console.log(goods_status);
      console.log(val)
      const data = {
        goods_status,
        count: val,
        opt: 'change_count'
      }
      api_updateCart(data).then(res => {
        console.log(res);
        this.select_data = []
        this.getCarts()
      }).catch(err => {
        console.log(err);
      })
    },
    getCarts() {
      api_getCart().then(res => {
        console.log('获取购物车数据', res);
        this.tableData = res.data.carts_list
        console.log(this.tableData);
        this.price_together = res.data.price_together
        for (let i of this.tableData) {
          if (i['is_select']) this.select_data.push(i)
        }
      }).catch(err => {
        console.log('获取购物车数据出错', err);
      })
    },
    deleteCart(goods_status) {
      const data = {
        goods_status
      }
      api_deleteCart(data).then(res => {
        console.log('删除购物车', res);
        this.$message({
          type: 'success',
          message: '删除成功',
          duration: 1000
        })
        this.select_data = []
        this.getCarts()
      }).catch(err => {
        console.log('删除购物车错误', err);
      })

    },
    goPay() {
      console.log('开始结算！')
      if (this.select_data.length===0) {
        this.$message({
          type: "warning",
          message: '暂无可结算商品'
        })
      } else {
        const data = {
          select_data:this.select_data
        }
        api_addOrderTemp(data).then(res => {
          console.log('添加订单临时存储', res);
          this.$router.push('/place_order')
        }).catch(err => {
          console.log('添加订单临时存储失败', err);
        })
      }
    },
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.cart_info_down {
  background-color: #FDF4E9;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  /*padding-bottom: 10px*/
}

.cart_info {
  border: #ECEEF4 solid 1px;
}
</style>
