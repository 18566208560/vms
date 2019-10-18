<template>
  <div>
    <el-row>
		<el-col :span="24" class="p_title">
			<span class="title">用户中心</span>
		</el-col>
	</el-row>
  <div v-if="msg">
    <table class="tablestyle01" >
       <tr>
            <td class="ltd" >姓名</td>
            <td>{{form.name}}</td>
        </tr>
      <tr>
            <td class="ltd">手机号</td>
            <td>{{form.phone}}</td>
        </tr>
      <tr>
            <td class="ltd">QQ</td>
            <td>{{form.qq}}</td>
        </tr>
      <tr>
            <td class="ltd">学校/企业名称</td>
            <td>{{form.adress}}</td>
        </tr>

    </table>

        <el-button style="margin-left:500px" type="primary" @click="msg=false">编&nbsp;&nbsp;&nbsp;&nbsp;辑</el-button>

    </div>
    <el-form ref="form" :model="form" label-width="110px" v-else >

      <el-form-item label="真实姓名">
        <el-input v-model="form.name" placeholder="请填写真实姓名"></el-input>
      </el-form-item>

      <el-form-item label="手机号码">
        <el-input v-model="form.phone" placeholder="请填写手机号码"></el-input>
      </el-form-item>

      <el-form-item label="QQ">
        <el-input v-model="form.qq" placeholder="请填写QQ号码"></el-input>
      </el-form-item>

      <el-form-item label="学校/企业名称">
        <el-input v-model="form.adress" placeholder="请填写学校或企业名称"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">提&nbsp;&nbsp;&nbsp;&nbsp;交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        userid:sessionStorage.user_id || localStorage.user_id,
        token:sessionStorage.token || localStorage.token,
        msg: false,
        form: {
          name: '',
          phone: '',
          qq: '',
          adress: ''
        },
      };
    },
    mounted() {
      this.get_info();
    },
    methods: {
      onSubmit() {
        this.axios.post(this.host + "/userinfo/" + this.userid, this.form,{
          responseType: 'json',
          headers: {'Authorization': 'JWT ' + this.token},
          withCredentials: true,
        }).then(response => {
          this.$message({
            type: 'info',
            message: '提交成功!'
          });
          this.$router.go(0)
        })
        .catch(error => {
          console.log(error, "error");
          this.$message({
            type: 'error',
            message: error.response.data.msg + '提交失败!'
          });

        });
      },
      get_info: function() {
        // 获取用户个人信息
        this.axios.get(this.host + '/userinfo/' + this.userid, {
          responseType: 'json',
          headers: {'Authorization': 'JWT ' + this.token},
          withCredentials: true, //跨域带上cookies
        }, ).then(response => {
          console.log(response.data)
            this.form.name = response.data.name;
            this.form.phone = response.data.phone;
            this.form.qq = response.data.qq;
            this.form.adress = response.data.adress;
            this.msg = true

        }).catch(error => {
          console.log(error.response.data);
          this.$message({
              type: 'info',
              message: '请填写个人信息！',
            })
        })
      },
    }
  }
</script>

<style scoped>
  .el-form {
    margin: 20px auto;
    width: 600px;
  }
  .tablestyle01{
      border:1px solid #8198ef;
      border-collapse:collapse;
      margin:50px auto;
  }
  .tablestyle01 td{
      border:1px solid #8198ef;
      color:#707171;
      text-align:center;
      width:600px;
      height:50px;
  }
  .tablestyle01 .ltd{
      text-align:left;
      text-indent:20px;
      width:250px;
  }

</style>
