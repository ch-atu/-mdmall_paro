<template>
  <div>
    <div style="height: 500px">
      <div style="font-size: 17px;margin-bottom: 10px;display: flex">修改密码</div>

      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="当前密码" prop="pre_pass">
          <el-input type="password" v-model="ruleForm.pre_pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPass">
          <el-input type="password" v-model="ruleForm.newPass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="newPass2">
          <el-input type="password" v-model="ruleForm.newPass2"></el-input>
        </el-form-item>
        <div style="display: flex; margin-left: 130px">
          <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import {changePass} from "@/api/user.request";
import Cookies from "js-cookie";

export default {
  name: "user_changePass",
  created() {
    this.$store.commit('app/CHANGE_ACTIVE', 'user_changePass')
  },
  data() {
    let checkPrePass = (rule, value, callback) => {
      callback()
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
      } else if (value !== this.ruleForm.newPass) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        pre_pass: '',
        newPass: '',
        newPass2: '',
      },
      rules: {
        pre_pass: [
          {validator: checkPrePass, trigger: 'blur'}
        ],
        newPass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        newPass2: [
          {validator: validatePass2, trigger: 'blur'}
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const user_id = this.$store.state.user.user_id
          let data = {
            password:this.ruleForm.pre_pass,
            new_password:this.ruleForm.newPass,
            new_password2:this.ruleForm.newPass2
          }
          changePass(data, user_id).then(res=>{
            this.$message({
              type:'success',
              message:'密码修改成功，请重新登录'
            })
            Cookies.remove('user_token')
            setTimeout(()=>{
              this.$router.push('/login')
              this.$store.commit('user/CLEAR')
            },2000)

          }).catch(err=>{
            console.log(err);
            this.$message({
              type:'error',
              message:err.response.data.non_field_errors[0]
            })
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.el-form-item {
  width: 350px;
}
.el-form{
  padding: 20px;
  border: #DDDDDD solid 1px;
}
</style>
