<template>
  <div style="min-height: 500px">
    <div class="home_title">
      <span style="font-size: 13px">您已创建了<em>{{ home_count }}</em>个收货地址，最多可以创建<em>20</em>个！</span>
      <el-button @click="dialogAddFormVisible = true" style="padding: 3px 6px;">新增收货地址</el-button>
    </div>

    <el-dialog title="新增收货地址" :visible.sync="dialogAddFormVisible" width="35%">
      <el-form :model="add_form" :rules="form_rules" ref="addRuleForm">
        <el-form-item label="收货人" label-width="100px" prop="receive">
          <el-input v-model="add_form.receive" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="所在地区" label-width="100px" prop="area">
          <el-input v-model="add_form.area" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="地址" label-width="100px" prop="address">
          <el-input v-model="add_form.address" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机号" label-width="100px" prop="mobile">
          <el-input v-model="add_form.mobile" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" label-width="100px" prop="email">
          <el-input v-model="add_form.email" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer" style="margin-top: -35px">
        <el-button @click="cancelAdd">取 消</el-button>
        <el-button type="primary" @click="addAddress('addRuleForm')">确 定</el-button>
      </div>
    </el-dialog>

    <div v-if="home_list.length !== 0">
      <div v-for="(home,index) in home_list" :key="home.id">
        <el-card style="margin-bottom: 15px">
          <div class="home_title_top">
            <div style="display: flex;align-items: center">
              <span style="font-size: 20px">{{ username }}</span>
              <span v-if="home.is_default" class="default_addr">默认收货地址</span>
            </div>
            <div style="">
              <el-button @click="edit(home)" style="padding: 3px 6px;margin-right: 10px">修改</el-button>
              <el-dialog title="修改收货地址" :visible.sync="dialogEditFormVisible" width="35%">
                <el-form :model="edit_form" :rules="form_rules" ref="editRuleForm">
                  <el-form-item label="收货人" label-width="100px" prop="receive">
                    <el-input v-model="edit_form.receive" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="所在地区" label-width="100px" prop="area">
                    <el-input v-model="edit_form.area" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="地址" label-width="100px" prop="address">
                    <el-input v-model="edit_form.address" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="手机号" label-width="100px" prop="mobile">
                    <el-input v-model="edit_form.mobile" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="邮箱" label-width="100px" prop="email">
                    <el-input v-model="edit_form.email" autocomplete="off"></el-input>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="cancelEdit">取 消</el-button>
                  <el-button type="primary" @click="editAddress('editRuleForm', index,home.id)">确 定</el-button>
                </div>
              </el-dialog>
              <el-popconfirm
                  icon="el-icon-info"
                  icon-color="red"
                  title="确定删除吗？"
                  @confirm="deleteOk(home.id)"
                  @cancel="deleteNo"
              >
                <el-button slot="reference" style="padding:3px 6px">删除</el-button>
              </el-popconfirm>
            </div>
          </div>
          <div class="home_title_main">
            <div>
              <span style="margin-left: 13px">收货人:</span><span>{{ home.receive }}</span>
            </div>
            <div>
              <span>所在地区:</span><span>{{ home.area }}</span>
            </div>
            <div>
              <span style="margin-left: 26px">地址:</span><span>{{ home.address }}</span>
            </div>
            <div>
              <span style="margin-left: 13px">手机号:</span><span>{{ home.mobile }}</span>
            </div>
            <div>
              <span style="margin-left: 26px">邮箱:</span><span>{{ home.email }}</span>
            </div>

          </div>
          <div class="home_title_down">
            <el-button type="text" style="padding: 0" @click="setDefault(home.id)">设为默认</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <el-empty description="暂无收货地址" STYLE="height: 399px" v-else></el-empty>
  </div>

</template>

<script>
import {getHome, addHome, editHome, deleteHome} from "@/api/user.request";
import {mapState} from "vuex";
import user from "@/store/modules/user";

export default {
  name: "user_home",
  created() {
    this.getHomeList()
    this.$store.commit('app/CHANGE_ACTIVE', 'user_home')
  },
  data() {
    let validateBlank = (rule, value, callback) => {
      if (!value) {
        callback(new Error('不能为空'))
      } else {
        callback()
      }
    };

    return {
      home_list: [],
      dialogAddFormVisible: false,
      dialogEditFormVisible: false,
      add_form: {
        receive: '',
        area: '',
        address: '',
        mobile: '',
        email: ''
      },
      form_rules: {
        receive: [
          {validator: validateBlank, trigger: 'blur'}
        ],
        area: [
          {validator: validateBlank, trigger: 'blur'}
        ],
        address: [
          {validator: validateBlank, trigger: 'blur'}
        ],
        mobile: [
          {validator: validateBlank, trigger: 'blur'}
        ],
        email: [
          {validator: validateBlank, trigger: 'blur'}
        ]
      },
      edit_form: {
        receive: '',
        area: '',
        address: '',
        mobile: '',
        email: ''
      },
    }
  },
  computed: {
    ...mapState('user', ['username', 'mobile', 'email']),
    home_count() {
      return this.home_list.length
    }
  },
  methods: {
    deleteOk(home_id) {
      deleteHome(home_id).then(res => {
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 1500
        })
        this.getHomeList()
      }).catch(err => {
        console.log(err);
      })
    },
    deleteNo() {
      this.$notify.info({
        title: '消息',
        message: '取消了操作',
        duration: 1500
      })
    },
    setDefault(home_id) {
      editHome({'is_default': true}, home_id).then(res => {
        console.log('修改默认地址', res)
        if (res.data.status === 0) {
          this.$message({
            type: 'warning',
            message: res.data.message,
            duration: 1000
          })
        } else {
          this.getHomeList()
          this.$message({
            type: 'success',
            message: '设置成功',
            duration: 1000
          })
        }
      }).catch(err => {
        console.log('修改默认地址错误', err);
      })
    },
    cancelAdd() {
      this.dialogAddFormVisible = false
      this.$notify.info({
        title: '消息',
        message: '取消了操作',
        duration: 1500
      })
    },
    addAddress(formName) {
      let data = this.add_form
      console.log(this.$refs);
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log('add_form', this.add_form);
          addHome(data).then(res => {
            this.dialogAddFormVisible = false
            this.$notify({
              type: 'success',
              title: '成功',
              message: '新增收货地址成功',
              duration: 1500
            })
            this.getHomeList()
            console.log('添加收货地址', res);
          }).catch(err => {
            this.dialogAddFormVisible = false
            console.log('添加收货地址出错', err);
          })
        }
      })
    },
    edit(home) {
      this.dialogEditFormVisible = true
      for (let key in this.edit_form) {
        this.edit_form[key] = home[key]
      }
      console.log(this.edit_form);
    },
    cancelEdit() {
      this.dialogEditFormVisible = false
      this.$notify.info({
        title: '消息',
        message: '取消了操作',
        duration: 1500
      })
    },
    editAddress(formName, index, home_id) {
      let data = this.edit_form
      this.$refs[formName][index].validate((valid) => {
        if (valid) {
          console.log('edit_form', this.edit_form);
          editHome(data, home_id).then(res => {
            this.dialogEditFormVisible = false
            this.$notify({
              type: 'success',
              title: '成功',
              message: '修改收货地址成功',
              duration: 1500
            })
            this.getHomeList()
            console.log('修改收货地址', res);
          }).catch(err => {
            this.dialogEditFormVisible = false
            console.log('修改收货地址出错', err);
          })
        }
      })
    },
    getHomeList() {
      getHome().then((res) => {
        console.log('获取收货地址', res);
        this.home_list = res.data
      }).catch(err => {
        console.log('获取收货地址错误', err);
      })
    }
  }
}
</script>

<style scoped>
@import "~@/css/main.css";

.el-form-item {
  width: 80%;
}

.el-dialog__body{
  padding-bottom: 100px;
}

.home_title {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.home_title span {
  font-size: 13px;
}

.home_title em {
  color: #ad522b;
}

.home_title_top {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 35px;
}

.default_addr {
  font-size: 10px;
  background-color: #e79807;
  color: white;
  padding: 5px 2px;
  margin-left: 20px
}

.home_title_main {
  margin-left: 30px;
  display: flex;
  flex-direction: column;
  align-items: flex-start
}

.home_title_main div {
  margin-bottom: 10px;
}

.home_title_main div span:first-child {
  margin-right: 15px;
  color: #999999;
}

.home_title_main div span {
  font-size: 13px;
}

.home_title_down {
  display: flex;
  justify-content: flex-end;
  font-size: 12px
}
</style>
