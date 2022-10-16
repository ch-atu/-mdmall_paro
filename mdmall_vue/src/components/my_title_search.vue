<template>
  <div class="user_center_up" style="margin-bottom: 20px">
    <el-row>
      <el-col :span="8">
        <div class="user_center_log">
          <el-link @click="$router.push('/')" :underline="false"> <img src="@/assets/images/logo.png" alt=""></el-link>
          <span>|&nbsp;&nbsp;&nbsp;&nbsp;{{ title }}</span>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="search">
          <el-input placeholder="请输入内容" v-model="search">
            <template slot="prepend"><i class="el-icon-search"></i></template>
          </el-input>
          <el-button type="primary" @click="searchGoods">搜索商品</el-button>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "my_title_search",
  props:['title'],
  data(){
    return{
      search:'',
    }
  },
  created() {
  },
  methods:{
    searchGoods(){
      if(!this.search){
        this.$message({
          message:'请输入要搜索的商品',
          duration:1000
        })
      }else {
        this.$router.push({path:'/search', query:{kw:this.search}})
        this.$store.commit('app/CHANGE_KW', this.search)
      }
    },
  }
}
</script>

<style scoped>
@import "~@/css/main.css";
.search {
  display: flex;
  height: 100px;
  align-items: center;
  justify-content: flex-end;
  margin-right: 10%;
}


</style>
