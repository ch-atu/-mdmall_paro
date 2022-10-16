<template>
  <div>
    <el-header height="150px">
      <el-link @click="$router.push('/')" :underline="false"><img src="@/assets/images/logo02.png" alt=""></el-link>
    </el-header>

    <el-main>
      <el-row>
        <el-col :span="15">
          <div style="display: flex;justify-content: center">
            <img src="@/assets/images/login_banner.png" alt="">
            <div
                style="width: 24px;font-size:24px;color:#f9dddd;text-align:center;line-height:30px;margin:20px 0 0 30px">
              商品美 · 种类多 · 欢迎光临
            </div>
          </div>

        </el-col>
        <el-col :span="7">
          <div class="login">
            <div class="login_title">账户登录</div>

            <div class="login_form">
              <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px"
                       class="demo-ruleForm">
                <el-form-item label="用户名" prop="username" size="medium">
                  <el-input type="text" v-model="ruleForm.username" autocomplete="off" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="checkPass" size="medium">
                  <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off" placeholder="请输入密码"></el-input>
                </el-form-item>
                <div style="text-align: left;margin: 0 0 30px 100px;">
                  <el-checkbox v-model="checked"></el-checkbox>
                  <span style="margin: 10px;font-size: 12px">记住登录</span>
                </div>
                <el-form-item style="margin-bottom: 0;padding-bottom: 20px">
                  <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
                  <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
              </el-form>
            </div>

            <div class="login_bottom">
              <div style="margin-left: 15px">其他登录方式</div>
              <div style="display: flex;">
                <img style="height: 20px;margin-right: 5px;" src="@/assets/images/right_icon.png" alt="">
                <el-link style="text-decoration: none;margin-right: 15px" href="/register">立即注册</el-link>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-main>

    <my-footer></my-footer>
  </div>
</template>

<script>
import MyFooter from '@/components/my_footer.vue'
import {login} from "@/api/user.request";
import Cookies from "js-cookie";

export default {
  name: "login",
  components: {MyFooter},
  created() {
    this.is_checked()
  },
  data() {
    let validateUsername = (rule, value, callback) => {
      callback()
    };
    let validatePass = (rule, value, callback) => {
      callback()
    };
    return {
      ruleForm: {
        username: localStorage.getItem('username'),
        checkPass: '',
      },
      rules: {
        username: [
          {validator: validateUsername, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass, trigger: 'blur'}
        ],
      },
      checked:true
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const data = {
            username: this.ruleForm.username,
            password: this.ruleForm.checkPass
          }
          login(data).then(res => {
            console.log('登录请求成功', res);
            this.$message({
              message: '登录成功',
              type: 'success',
              duration: 1000
            })
            Cookies.set('user_token', res.data.token)
            if(this.checked){
              localStorage.setItem('username', this.ruleForm.username)
            }else {
              localStorage.removeItem('username')
            }
            localStorage.setItem('remember', this.checked.toString())
            this.$router.push('/')
          }).catch(err => {
            this.$message({
              type:"error",
              message:'用户名或密码错误',
              duration:1500
            })
            console.log('登录请求失败', err);
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    is_checked() {
      const remember = localStorage.getItem('remember')
      this.checked = remember !== 'false';
    },
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.el-footer {
  /*background-color: #B3C0D1;*/
  color: #333;
  text-align: center;
}

.el-header {
  display: flex;
  align-items: center;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  padding: 0;
}

.el-form-item {
  width: 350px;
}

.el-row {
  background-color: #76150D;
}
</style>
