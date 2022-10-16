<template>
  <div>
    <my-header></my-header>
    <my-title-search title="用户中心"></my-title-search>

    <el-container>
      <el-aside style="background-color: #F3F3F3;width: 200px; margin: 0 0 20px 100px;">
        <el-menu
            :default-active="active_data"
            class="el-menu-vertical-demo"
            background-color="#F3F3F3"
            @select="select_menu">
          <el-menu-item index="user_info">
            <i class="el-icon-location"></i>
            <span>个人信息</span>
          </el-menu-item>
          <el-menu-item index="user_order">
            <i class="el-icon-menu"></i>
            <span slot="title">全部订单</span>
          </el-menu-item>
          <el-menu-item index="user_home">
            <i class="el-icon-document"></i>
            <span slot="title">收货地址</span>
          </el-menu-item>
          <el-menu-item index="user_changePass">
            <i class="el-icon-setting"></i>
            <span slot="title">修改密码</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main style="padding: 0 20px;margin-bottom: 20px">
        <router-view></router-view>
      </el-main>
    </el-container>


    <my-footer></my-footer>

  </div>


</template>

<script>
import MyHeader from '@/components/my_header'
import MyFooter from '@/components/my_footer'
import MyTitleSearch from '@/components/my_title_search'
import {mapState} from "vuex";

export default {
  name: "user_center",
  components: {
    MyHeader,
    MyFooter,
    MyTitleSearch
  },
  created() {
  },
  data() {
    return {
    }
  },
  computed:{
    ...mapState('app', ['active_data'])
  },
  methods: {
    select_menu(index) {
      if (index === 'user_info') {
        this.$router.push('/user_center/' + index)
      } else if (index === 'user_home') {
        this.$router.push('/user_center/' + index)
      } else if (index === 'user_order') {
        this.$router.push('/user_center/' + index)
      } else if (index === 'user_changePass') {
        this.$router.push('/user_center/' + index)
      }
    },
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.el-input {
  width: 450px;
}

</style>
