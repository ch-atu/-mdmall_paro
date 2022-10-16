<template>
  <div>
    <my-header></my-header>
    <my-title-search title="搜索结果"></my-title-search>
    <el-main>
      <div class="index_goods" v-for="item in goods_list">
        <div>
          <el-button type="text" class="index_goods_btn" @click="toDetail(item.id, item.category_name, item.category_id)">
            <img :src="item.image" alt="" style="background-color: #f9dddd;">
            <a :title="item.name">{{ item.name }}</a>
          </el-button>
        </div>
        <span>￥ </span>
        <span>{{ item.price }}</span>
      </div>
    </el-main>
    <el-pagination
        background
        layout="prev, pager, next, total, jumper"
        :total="page_total"
        :page-size="5"
        @current-change="changePage"
        style="margin-bottom: 20px">
    </el-pagination>
    <my-footer></my-footer>
  </div>
</template>

<script>
import MyHeader from '@/components/my_header'
import MyFooter from '@/components/my_footer'
import MyTitleSearch from '@/components/my_title_search'
import {api_goodsSearch} from "@/api/goods.request";
import {mapState} from "vuex";


export default {
  name: "search",
  components: {
    MyHeader,
    MyFooter,
    MyTitleSearch
  },
  created() {
    this.getSearchGoods()
  },
  data() {
    return {
      page_total: 0,
      goods_list: []
    }
  },
  computed:{
    ...mapState('app',['kw'])
  },
  watch:{
    kw:function (){
      console.log('kw的值发生变化了');
      this.getSearchGoods()
    }
  },
  methods: {
    getSearchGoods(page=1) {
      let kw = this.$route.query.kw
      if (!kw) {
        this.goods_list = []
      } else {
        api_goodsSearch(kw, page).then(res => {
          this.page_total = res.data.count
          this.goods_list = res.data.results
          console.log('搜索商品响应', res);
        }).catch(err => {
          console.log('搜索商品失败', err);
        })
      }
    },
    changePage(page) {
      console.log(page);
      this.getSearchGoods(page)
    },
    toDetail(id, name, category_id) {
      console.log('商品类别', name);
      this.$router.push({path: '/detail', query: {goods_id: id, category_id, category: name}})
    }
  }
}
</script>

<style scoped>
.el-main {
  padding: 0 0 0 8%;
  /*background-color: #99a9bf;*/
  margin: 10px 100px 20px 100px;
  display: flex;
  /*justify-content: center;*/
  /*align-items: flex-end;*/
  flex-wrap: wrap;
  /*border-left: #b2b4b6 solid 1px;*/
  /*border-right: #b2b4b6 solid 1px;*/
  /*border-top: #b2b4b6 solid 1px;*/
}

.index_goods {
  /*background-color: #f9dddd;*/
  width: 12.5%;
  height: 200px;
  /*border-bottom: #b2b4b6 solid 1px;*/
  /*border-left: #b2b4b6 solid 1px;*/
  border: #b2b4b6 solid 1px;
  /*margin-left: -1px;*/
  margin: 15px 30px 15px 30px;
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
  width: 100%;
}

.index_goods span {
  color: red;
}

.index_goods img {
  margin-top: 10px;
  width: 85%;
  /*width: 100%;*/
  /*height: 10%;*/
}
</style>
