<template>
  <div>
    <el-main>
      <el-row>
        <el-col :span="11">
          <div style="float: right;padding-right: 20px;">
            <a href="/"><img src="@/assets/images/logo.png" alt=""></a>
            <div class="reg_slogan">商品美 · 种类多 · 欢迎光临</div>
            <img style="opacity: 0.5;" src="@/assets/images/register_banner.png" alt="">
          </div>
        </el-col>
        <el-col :span="7">
          <div class="register_title">
            <h1>用户注册</h1>
            <div style="display: flex;justify-content: right">
              <img style="height: 20px;margin-right: 5px;" src="@/assets/images/right_icon.png" alt="">
              <el-link href="/login">登录</el-link>
            </div>

          </div>

          <div class="register_form">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" size="medium">
              <el-form-item label="用户名" prop="username">
                <el-input type="text" v-model="ruleForm.username" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="ruleForm.checkPass"></el-input>
              </el-form-item>
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model.number="ruleForm.mobile"></el-input>
              </el-form-item>
              <el-form-item label="短信验证码" prop="code" style="width: 450px;">
                <el-input v-model="ruleForm.code" style="width: 150px; float:left"></el-input>
                <el-button style="font-size: 10px;padding: 10px;float: left;margin-left: 22px"
                           @click="send_sms"
                           :disabled="sending_flag">
                  {{ sms_code_tip }}
                </el-button>
              </el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">立即注册</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form>
          </div>
        </el-col>
      </el-row>
    </el-main>

    <my-footer></my-footer>
  </div>
</template>

<script>
import MyFooter from '@/components/my_footer'
import {register, checkUser, checkTel} from "@/api/user.request";
import Cookies from 'js-cookie'

export default {
  name: "register",
  components: {
    MyFooter
  },
  data() {
    let checkUsername = (rule, value, callback) => {
      // const pattern = /^[a-zA-Z0-9_@\-+]{5,20}$/;
      const pattern = /^[\u4E00-\u9FA5A-Za-z0-9_]+$/;
      if (!value) {
        return callback(new Error('请输入用户名'))
      } else if (value.length < 2 || value.length > 20) {
        return callback(new Error('至少输入三个字符的用户名'))
      }
      else if (!pattern.test(value)) {
        return callback(new Error('用户名由中英文、数字、_、构成'))
      }
      else {
        checkUser(this.ruleForm["username"]).then(res => {
          console.log(res)
          if (res.data.count === 1) {
            callback(new Error('该用户名已存在'))
          } else {
            callback()
          }
        }).catch(err => {
          console.log(err);
        })
      }
    };
    let validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else if (value.length < 8 || value.length > 20) {
        callback(new Error('请输入8-20位密码'))
      } else {
        callback();
      }
    };
    let validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    let checkMobile = (rule, value, callback) => {
      const pattern = /^1[3-9]\d{9}/
      if (!value) {
        this.error_mobile = true
        callback(new Error('请输入手机号'))
      } else if (!pattern.test(value)) {
        this.error_mobile = true
        callback(new Error('请输入正确的手机号格式'))
      } else {
        // 判断手机号是否被注册
        checkTel(this.ruleForm["mobile"]).then(res => {
          console.log('手机号', res);
          if (res.data.count === 1) {
            this.error_mobile = true
            callback(new Error('该手机号已被注册'))
          } else {
            this.error_mobile = false
            callback()
          }
        }).catch(err => {
          console.log(err);
        })
      }
    };
    let checkCode = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入验证码'))
      } else {
        !this.error_code ? callback() : callback(new Error('验证码错误'));
      }
    };

    return {
      ruleForm: {
        username: '',
        pass: '',
        checkPass: '',
        mobile: '',
        code: ''
      },
      rules: {
        username: [
          {validator: checkUsername, trigger: 'blur'}
        ],
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass2, trigger: 'blur'}
        ],
        mobile: [
          {validator: checkMobile, trigger: 'blur'}
        ],
        code: [
          {validator: checkCode, trigger: 'blur'}
        ],
      },
      error_mobile: false,
      error_code: false,
      sms_code_tip: '获取短信验证码',
      sending_flag: false,
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = {
            username: this.ruleForm["username"],
            password: this.ruleForm["pass"],
            password2: this.ruleForm["checkPass"],
            mobile: this.ruleForm["mobile"],
            code: this.ruleForm["code"]
          }
          register(data).then(res => {
            console.log('注册成功后返回数据', res);
            Cookies.set('user_token', res.data.token)
            this.$message({message: '注册成功，2秒后自动跳转至首页', type: 'success',duration:2000})
            setTimeout(() => this.$router.push('/'), 2000)
          }).catch(err => {
            console.log('注册失败', err);
            this.$message.error('注册失败')
            this.$refs[formName].validateField('code')
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
    send_sms() {
      // 表示后端发送短信成功
      // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
      this.$refs['ruleForm'].validateField('mobile')
      if (this.error_mobile) return;
      this.sending_flag = true
      let num = 60;
      // 设置一个计时器
      let t = setInterval(() => {
        if (num === 1) {
          // 如果计时器到最后, 清除计时器对象
          clearInterval(t);
          // 将点击获取验证码的按钮展示的文本回复成原始文本
          this.sms_code_tip = '获取短信验证码';
          // 将点击按钮的onclick事件函数恢复回去
          this.sending_flag = false;
        } else {
          console.log(t);
          num -= 1;
          // 展示倒计时信息
          this.sms_code_tip = num + '秒';
        }
      }, 1000, 60)
    }
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.el-form-item {
  width: 380px;
}

.register_title {
  height: 70px;
  /*padding-left: 195px;*/
  display: flex;
  justify-content: space-between;
  align-items: center;

}

.register_title h1 {
  /*height: 50px;*/
  /*line-height: 50px;*/
  font-size: 24px;
  color: #a8a8a8;
  margin-left: 0
}

.register_title a {
  text-decoration: none;
  margin-right: 10px;
}

.register_form {
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.reg_slogan {
  width: 300px;
  height: 30px;
  text-align: right;
  font-size: 22px;
  color: #fe0000;
  margin: 20px 0;
}
</style>
