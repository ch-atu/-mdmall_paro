<template>
    <el-row>
      <el-col :span="7">
        <div class="index_logo">
          <el-link :underline="false" @click="$router.push('/')">
            <img src="@/assets/images/logo.png" alt="">
          </el-link>
        </div>
      </el-col>
      <el-col :span="10">
        <div class="search">
          <el-input placeholder="请输入内容" v-model="search">
            <template slot="prepend"><i class="el-icon-search"></i></template>
          </el-input>
          <el-button type="primary" @click="searchGoods">搜索商品</el-button>
        </div>
      </el-col>
      <el-col :span="7">
        <div class="index_cart">
          <div class="cart_logo">
            <i class="el-icon-shopping-cart-full"></i>
            <span>购物车</span>
          </div>
          <h4>{{count}}</h4>
        </div>
      </el-col>
    </el-row>
</template>

<script>
import {api_getCartCount} from "@/api/cart.request";
import {mapState} from "vuex";

export default {
  name: "my_title_search_cart",
  created() {
    this.getCarts()
  },
  data(){
    return {
      search: "",
    }
  },
  computed:{
    ...mapState('cart', ['count', ])
  },
  methods:{
    getCarts() {
      api_getCartCount().then(res =>{
        console.log('首页详情页获取购物车', res);
        const count = res.data.count
        this.$store.commit('cart/RESETCOUNT', count)
      }).catch(err=>{
        console.log('首页详情页获取购物车失败', err);
      })
    },
    searchGoods() {
      if (!this.search) {
        this.$message({
          message: '请输入要搜索的商品',
          duration: 1000
        })
      } else {
        this.$router.push({path: '/search', query: {kw: this.search}})
        this.$store.commit('app/CHANGE_KW', this.search)
      }
    },
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.index_logo {
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center
}

.search {
  display: flex;
  height: 100px;
  align-items: center;
  justify-content: flex-end;
  margin-right: 10%;
}

.index_cart {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center
}

.index_cart span {
  margin: 0 10px
}

.index_cart h4 {
  background-color: red;
  color: white;
  line-height: 40px;
  height: 40px;
  width: 40px
}

.cart_logo {
  width: 100px;
  height: 40px;
  border: #e5e9f2 solid 1px;
  /*background-color: #e5e9ff;*/
  display: flex;
  justify-content: center;
  align-items: center
}

</style>
