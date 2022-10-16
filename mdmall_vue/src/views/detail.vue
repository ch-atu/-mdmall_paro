<template>
  <div>
    <my-header></my-header>

    <my-title-search-cart></my-title-search-cart>

    <el-main style="margin: 0 6% 20px 6%; border: #EDEDED solid 1px">
      <el-row>

        <el-col :span="9">
          <img :src="goods.image" alt=""
               style="width: 350px;height: 350px;margin:45px 0;border: #EDEDED solid 1px">
        </el-col>

        <el-col :span="15" style="">
          <div class="detail_title">
            <H3 style="margin: 0 0 10px 0">{{ goods.name }}</H3>
            <span style="font-size: 12px;text-align: left">{{ goods.account }}</span>
          </div>

          <div class="detail_title_down_box">
            <h1 style="color: red;margin: 10px 10px 0 10px;">￥ {{ goods.price }}</h1>
            <div style="display: flex;align-items: flex-end;margin-bottom: 5px">
              <span> | <span style="color: #597DE9;margin-left: 8px">499</span> 人评价</span>
            </div>
          </div>

          <div class="detail_opt">
            <div>
              <span style="margin-right: 56px">数量:</span>
              <el-input-number v-model="opt_num" :min="1" size="small"></el-input-number>
            </div>

            <div>
              <span style="margin-right: 30px">产品规格:</span>
              <el-select v-model="select_value" placeholder="请选择" @change="changeSelect">
                <el-option
                    v-for="item in specifications"
                    :key="item.id"
                    :label="item.specification"
                    :value="item.id">
                </el-option>
              </el-select>
            </div>

            <div>
              <span style="margin-right: 15px">总价:</span>
              <span style="color: red;font-size: 18px">{{ goods.price }}元</span>
            </div>
          </div>

          <div style="display: flex;margin: 30px 0 10px 30px;">
            <el-button type="danger" style="height: 50px;width: 130px" @click="addCart">
              加入购物车
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-main>

    <el-main style="margin:0 6% 0 6%;height: 600px;">
      <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          @select="handleSelect"
          background-color="#EDEDED"
          active-text-color="#343131">
        <el-menu-item index="1">商品详情</el-menu-item>
        <el-menu-item index="2">规格与包装</el-menu-item>
        <el-menu-item index="3">商品评价(2)</el-menu-item>
        <el-menu-item index="4">售后服务</el-menu-item>
      </el-menu>

      <div class="goods_detail" v-if="activeIndex==='1'">
        <div>
          <span style="color: #76150D;font-size: 18px;margin: 10px 0">商品详情:</span>
          <span style="text-align: left;font-size: 15px">{{ goods.detail }}</span>
        </div>
      </div>
      <div class="goods_size" v-if="activeIndex==='2'">
        <div>
          <span style="color: #76150D;font-size: 18px;margin: 10px 0">规格与包装:</span>
          <span style="text-align: left;font-size: 15px">{{ goods.packing }}</span>
        </div>
      </div>
      <div class="goods_estimate" v-if="activeIndex==='3'">
        <div style="border-bottom: #EDEDED solid 1px;" v-for="i in 3">
          <el-row>
            <el-col :span="5">
              <div style="display: flex;align-items: center;margin: 20px 0">
                <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
                <span style="margin-left: 15px">chatu</span>
              </div>
            </el-col>
            <el-col :span="19">
              <div style="display: flex;flex-direction: column;align-items: flex-start;">
                <el-rate
                    v-model="value"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                    style="margin-top: 25px">
                </el-rate>
                <span style="font-size: 13px;text-align: left;margin: 10px 0 20px 0">派送非常快，第二天上午就收到。2天使用初步总结，前一部手机也是华为P9plus.MATE10pro包装原封未拆精致大气。拆开后第一眼就看到宝石蓝的手机，非常惊艳；然后就是配件一应俱全。开机各方面设置，把通讯录、短信等同步好，同品牌手机同步很快。和P9plus一样的后置指纹识别很方便。录制指纹容易，解锁非常快，秒开！屏幕完好，默认分辨率显示效果很好。</span>
              </div>
            </el-col>
          </el-row>
        </div>
        <el-pagination
            background
            layout="prev, pager, next, total,jumper"
            :total="1000"
            style="margin-top: 20px;">
        </el-pagination>
      </div>
      <div class="after_sale" v-if="activeIndex==='4'">
        <div>
          <span style="color: #76150D;font-size: 18px;margin: 10px 0">售后服务:</span>
          <span style="text-align: left;font-size: 15px">{{ goods.service }}</span>
        </div>
      </div>
    </el-main>

    <my-footer></my-footer>
  </div>
</template>

<script>
import MyFooter from '@/components/my_footer'
import MyHeader from '@/components/my_header'
import MyTitleSearchCart from '@/components/my_title_search_cart'
import {getGoodDetail} from "@/api/goods.request";
import {api_addCart} from "@/api/cart.request";
import {api_getCartCount} from "@/api/cart.request";
import {addHistory} from "@/api/user.request";

export default {
  name: "detail",
  components: {
    MyFooter,
    MyHeader,
    MyTitleSearchCart
  },
  data() {
    return {
      opt_num: 1,
      activeIndex: '3',
      value: 3.7,
      select_value:'',
      specifications: [],
      goods : '',
    };
  },
  created() {
    console.log(this.$route.query.goods_id);
    console.log(this.$route.query.category);
    const good_id = this.$route.query.goods_id
    const category = this.$route.query.category
    const category_id = this.$route.query.category_id
    getGoodDetail(good_id, category).then(res=>{
      console.log('详情数据', res);
      this.goods = res.data
      this.specifications = res.data.specifications
      this.select_value = this.specifications[0].id

      //添加历史记录
      addHistory({good_id, category_id:this.goods.category_id.toString()}).then(res=>{
        console.log('添加历史记录成功', res);
      }).catch(err=>{
        console.log('添加历史记录失败', err);
      })
    }).catch(err=>{
      this.$router.push('/')
    })
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      this.activeIndex = key
      console.log(typeof key);
    },
    changeSelect(val){
      console.log('下拉框选中值',val);
      console.log(this.select_value);
    },
    addCart(){
      console.log(this.$store.state.user.username);
      if(!this.$store.state.user.username){
        this.$message({
          type:'warning',
          message:'请先登录再操作',
          duration:1500
        })
      }else {
        console.log('添加购物车',this.goods);
        const data = {
          goods_id: this.goods.id,
          category_id:this.goods.category_id,
          specification_id:this.select_value,
          count: this.opt_num,
        }
        api_addCart(data).then(res=>{
          this.$message({
            type:"success",
            message:'添加购物车成功'
          })
          console.log('添加购物车响应',res);
          // 添加购物车成功后重新获取购物车总数量
          api_getCartCount().then(res =>{
            const count = res.data.count
            this.$store.commit('cart/RESETCOUNT', count)
          }).catch(err=>{
            console.log('首页详情页获取购物车失败', err);
          })
        }).catch(err=>{
          console.log('添加购物车出错', err);
        })
      }
    }
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.detail_title {
  display: flex;
  flex-direction: column;
  align-items: flex-start
}

.detail_title_down_box {
  display: flex;
  justify-content: space-between;
  background-color: #FDF5F5;
  margin-bottom: 15px;
}

.detail_opt div {
  display: flex;
  align-items: center;
  font-size: 13px;
  margin-bottom: 35px;
}

.detail_opt div div{
  margin-bottom: 0;
}


.goods_detail div, .goods_size div, .after_sale div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  color: #666666;
  font-size: 13px;
}

</style>
