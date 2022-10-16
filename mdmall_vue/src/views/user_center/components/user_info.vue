<template>
  <div>
    <!--    基本信息-->
    <div class="info_title">
      <span>基本信息</span>
    </div>
    <el-card>
      <div class="user_info_card" style="font-size: 15px">
        <div><span>用户名:</span><span>{{ username }}</span></div>
        <div><span>手机号:</span><span>{{ mobile }}</span></div>
        <div style="display: flex">
          <div>
            <span style="margin-left: 16px">邮箱:</span><span>{{ user_email }}</span>
          </div>
          <el-button v-if="!email" type="text" @click="open" style="padding-top: 4px;margin-left: -30px">添加邮箱
          </el-button>
          <div v-else-if="!email_active">
            <el-button type="text" @click="toActive" style="padding: 0;margin-left: -30px">点击激活</el-button>
            <span style="margin-left: -39px">(若已激活请刷新页面重试)</span>
          </div>
          <div v-else style="margin-left: -30px">
            <span style="font-size: 13px;color:#42b983;margin-right: 6px">已激活</span>
            <i class="el-icon-check" style="color: #42b983; font-size: 18px"></i>
          </div>
        </div>
      </div>
    </el-card>

    <!--      最近浏览-->
    <div class="view_title">
      <span>最近浏览</span>
    </div>
    <div style="display: flex; margin-bottom: 60px">
      <div class="view_goods" v-for="goods in history_goods_list" :key="goods.id">
        <el-button type="text" style="padding: 0"
                   @click="toDetail(goods.goods_id, goods.category_name, goods.category_id)">
          <img :src="goods.goods_img" alt="" style="width: 130px;height: 130px">
          <a :title="goods.goods_name">{{ goods.goods_name }}</a>
        </el-button>
        <div style="display: flex;justify-content: space-between">
          <span style="color: red">{{ goods.goods_price }} 元</span>
          <el-button type="text" style="padding: 0"
                     @click="addCart(goods.goods_id, goods.category_id, goods.specifications_id)">
            <i style="margin-top: 3px" class="el-icon-shopping-cart-2"></i>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";
import {addEmail, activeEmail} from "@/api/user.request";
import {getHistory, api_checkEmail} from "@/api/user.request";
import {api_addCart} from "@/api/cart.request";

export default {
  name: "user_info",
  created() {
    this.$store.commit('app/CHANGE_ACTIVE', 'user_info')
    this.getUserHistory()
  },
  data() {
    return {
      history_goods_list: [],
      email_status : true
    }
  },
  computed: {
    ...mapState('user', ['username', 'mobile', 'email_active', 'email']),
    user_email() {
      if (!this.$store.state.user.email) {
        return '未添加邮箱！'
      } else {
        return this.$store.state.user.email
      }
    }
  },
  methods: {
    open() {
      this.$prompt('请输入邮箱', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^([a-zA-Z\d])(\w|\-)+@[a-zA-Z\d]+\.[a-zA-Z]{2,4}$/,
        inputErrorMessage: '邮箱格式不正确',
      }).then(({value}) => {
        const data = {
          email: value
        }
        addEmail(data).then(res => {
          console.log('添加邮箱', res);
          if(res.data.count){
            this.$message({
              type: 'error',
              message: '邮箱已被占用'
            });
          }else {
            this.$store.state.user.email = res.data.email
            this.$message({
              type: 'success',
              message: '添加成功'
            });
          }
        }).catch(err => {
          console.log('添加邮箱失败', err);
        })
      }).catch(() => {
        this.$notify({
          type: 'info',
          title: '消息',
          message: '取消输入',
          duration: 1500
        });
      });
    },
    toActive() {
      activeEmail().then(res => {
        console.log('邮箱激活成功', res);
      }).catch(err => {
        console.log('邮箱激活失败', err);
      })
      this.$message({
        type: "success",
        message: '已发送激活邮件',
        duration: 1500
      })
    },
    getUserHistory() {
      getHistory().then(res => {
        this.history_goods_list = res.data.his_goods_data
        console.log('获取历史记录成功', res);
      }).catch(err => {
        console.log('获取历史记录失败', err);
      })
    },
    toDetail(goods_id, category_name, category_id) {
      console.log('商品类别', name);
      this.$router.push({path: '/detail', query: {goods_id, category_id, category: category_name}})
    },
    addCart(goods_id, category_id, specification_id) {
      console.log('添加购物车');
      const data = {
        goods_id,
        category_id,
        specification_id,
        count: 1,
      }
      api_addCart(data).then(res => {
        this.$message({
          type: "success",
          message: '添加购物车成功'
        })
        console.log('添加购物车响应', res);
      }).catch(err => {
        console.log('添加购物车出错', err);
      })
    }
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

</style>
