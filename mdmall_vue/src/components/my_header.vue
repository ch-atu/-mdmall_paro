<template>
  <div class="header_con">
    <el-row>
      <el-col :span="5">
        <div class="welcome">欢迎来到美多商城！</div>
      </el-col>
      <el-col :span="19">
        <el-row>
          <el-col :span="15" v-if="showMsg">
            <div class="login_info">
              欢迎您：<em>{{ username }}</em>
              <span>|</span>
              <el-link :underline="true" type="danger" @click="logOut">退出</el-link>
            </div>
          </el-col>
          <el-col :span="15" v-if="!showMsg">
            <div class="login_btn">
              <el-link href="/login">登录</el-link>
              <span>|</span>
              <el-link href="/register">注册</el-link>
            </div>
          </el-col>
          <el-col :span="9">
            <div class="user_link">
              <el-link @click="$router.push('/user_center/user_info')">用户中心</el-link>
              <span>|</span>
              <el-link @click="$router.push('/cart')">我的购物车</el-link>
              <span>|</span>
              <el-link @click="$router.push('/user_center/user_order')">我的订单</el-link>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {mapState,} from 'vuex'
import {getUser} from "@/api/user.request";
import Cookies from "js-cookie";

export default {
  name: "my_header",
  created() {
    // console.log('进来header');
    if (this.username) {
      this.showMsg = true;
    }
  },
  data() {
    return {
      showMsg: false,
    }
  },
  computed: {
    ...mapState('user', ['username',]),
  },
  methods: {
    logOut() {
      Cookies.remove('user_token')
      this.$store.commit('user/CLEAR')
      this.$store.commit('cart/CLEAR')
      this.$router.push('/login')
    }
  },
}
</script>

<style scoped>
@import "~@/css/main.css";

.el-link {
  font-size: 12px;
}

.welcome, .login_info, .login_btn, .user_link {
  line-height: 29px;
}

.login_btn, .login_info {
  float: right;
}

.header_con {
  background-color: #f7f7f7;
  height: 29px;
  border-bottom: 1px solid #dddddd;
  font-size: 12px;
  color: #666;
}

.login_btn span, .user_link span, .login_info span {
  margin: 0 20px;
}

</style>
