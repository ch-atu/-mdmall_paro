<template>
  <div>
    <my-header></my-header>
    <el-result icon="success" title="成功提示" subTitle="您已激活成功" v-if="is_active">
      <template slot="extra">
        <el-button type="primary" size="medium">返回首页</el-button>
      </template>
    </el-result>

    <el-result icon="error" title="错误提示" subTitle="未成功激活" v-else>
      <template slot="extra">
        <el-button type="primary" size="medium">返回首页</el-button>
      </template>
    </el-result>
    <my-footer></my-footer>
  </div>
</template>

<script>
import MyHeader from "@/components/my_header";
import MyFooter from "@/components/my_footer";
import {checkActiveEmail} from "@/api/user.request";
import Cookies from "js-cookie";

export default {
  name: "active",
  components:{
    MyHeader,
    MyFooter
  },
  data(){
    return {
      is_active:false,
    }
  },
  created() {
    console.log(this.$route);
    this.checkEmailToken(this.$route.query.token)
  },
  methods:{
    checkEmailToken(token){
      checkActiveEmail(token).then(res=>{
        console.log('邮箱激活成功', res);
        if(res.status ===200 && this.$store.state.user.username===res.data.username){
          this.is_active = true
          this.$store.state.user.email_active = true
        }else {
          this.$message({
            message:'登录环境发生变化，请重新登录',
            duration:1500
          })
          Cookies.remove('user_token')
          this.$store.commit('user/CLEAR')
          this.$store.commit('cart/CLEAR')
          this.$router.push('/login')
        }
      }).catch(err=>{
        console.log('邮箱激活失败', err);
      })
    }
  }
}
</script>

<style scoped>

</style>
