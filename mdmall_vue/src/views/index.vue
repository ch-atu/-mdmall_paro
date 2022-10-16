<template>
  <div>
    <my-header></my-header>

    <my-title-search-cart></my-title-search-cart>

    <el-carousel height="350px" style="margin-top: 20px">
      <el-carousel-item v-for="item in 3" :key="item">
        <img src="~@/assets/images/slide01.jpg" alt="">
      </el-carousel-item>
    </el-carousel>

    <div class="goods_category" v-for="item in goods" :key="item.id">
      <div class="index_title">
        <span>{{ item.id }}F {{ item.name }}</span>
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">时尚新品</el-menu-item>
          <el-menu-item index="2">手机配件</el-menu-item>
          <el-menu-item index="3">畅享低价</el-menu-item>
          <el-menu-item index="4">精选单品</el-menu-item>
        </el-menu>
      </div>
      <el-main>
        <div class="index_goods" v-for="each_good in item.goods_list">
          <div @click="toDetail(each_good.id, item.name, each_good.category)">
            <el-button type="text" class="index_goods_btn">
              <img :src="each_good.image" alt="">
              <a :title="each_good.name">{{ each_good.name }}</a>
            </el-button>
          </div>
          <span>￥ </span>
          <span>{{ each_good.price }}</span>
        </div>
      </el-main>
      <br>
    </div>

    <my-footer></my-footer>
  </div>
</template>

<script>
import MyHeader from '@/components/my_header'
import MyFooter from '@/components/my_footer'
import MyTitleSearchCart from '@/components/my_title_search_cart'
import {getMobiles, getComputers} from "@/api/goods.request";

export default {
  name: "index",
  components: {
    MyHeader,
    MyFooter,
    MyTitleSearchCart
  },
  async created() {
    await getMobiles().then(res => {
      console.log('获取的手机商品数据', res);
      let mobiles = {
        id: 1,
        name: '手机通讯',
        goods_list: res.data.slice(0, 16)
      }
      this.goods.push(mobiles)
    }).catch(err => {
      console.log('请求错误', err);
    });
    await getComputers().then(res => {
      console.log('获取电脑商品数据', res);
      let computers = {
        id: 2,
        name: '电脑设备',
        goods_list: res.data.slice(0, 16)
      }
      this.goods.push(computers)
    }).catch((err) => {
      console.log('请求出错', err);
    })
  },
  data() {
    return {
      activeIndex: '1',
      goods: []
    }
  },
  methods: {
    handleSelect(key, keypath) {
      console.log(key, keypath)
    },
    toDetail(id, name, category_id) {
      console.log('商品类别', name);
      this.$router.push({path: '/detail', query: {goods_id: id, category_id, category: name}})
    }
  }
}


</script>

<style scoped>
@import "~@/css/main.css";

.el-main {
  padding: 0;
  /*background-color: #99a9bf;*/
  margin: 10px 100px 20px 100px;
  display: flex;
  flex-wrap: wrap;
  border-left: #b2b4b6 solid 1px;
  border-right: #b2b4b6 solid 1px;
  border-top: #b2b4b6 solid 1px;
}

.el-input {
  width: 450px;
}


.index_goods {
  /*background-color: #f9dddd;*/
  width: 12.5%;
  height: 200px;
  border-bottom: #b2b4b6 solid 1px;
  border-left: #b2b4b6 solid 1px;
  margin-left: -1px;
}

.index_goods a {
  font-size: 13px;
  color: #666;
  font-weight: normal;
  line-height: 24px;
  width: 130px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  display: block;
  margin: 0 auto;
  text-decoration: none;
}

.index_goods_btn {
  padding: 0;
  /*display: block;*/
  /*margin: 0 auto*/
}

.index_goods span {
  color: red;
}

.index_goods img {
  margin-top: 10px;
  width: 85%;
  /*height: 10%;*/
}

.index_title {
  /*border-bottom: #e5e9f2 solid 1px;*/
  /*background-color: #99a9bf;*/
  height: 61px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 100px;
}

</style>
