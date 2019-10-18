<template>
  <div>
    <h1 style="text-align: center">注&nbsp;&nbsp;册</h1>
    <el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2" label-width="100px" class="demo-ruleForm">

      <el-form-item label="用 户 名" prop="user">
        <el-input placeholder="请输入6-12位英文或数字字符" type="text" v-model="ruleForm2.user" auto-complete="off"></el-input>
      </el-form-item>

      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm2.pass" auto-complete="off" placeholder="请输入由数字或字母组成的6-12个字符"></el-input>
      </el-form-item>

      <el-form-item label="确认密码" prop="pass2">
        <el-input type="password" v-model="ruleForm2.pass2" auto-complete="off"></el-input>
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input placeholder="用于密码找回" type="text" v-model="ruleForm2.email" auto-complete="off"></el-input>
      </el-form-item>

      <el-form-item label="验 证 码" prop="captcha">
        <el-input type="text" v-model.number="ruleForm2.captcha">
          <el-button slot="append"><img :src="captcha_url" @click="generate_captcha" alt=""></el-button>b bv
        </el-input>
      </el-form-item>


      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm2')">注&nbsp;&nbsp;册</el-button>
        <el-button @click="resetForm('ruleForm2')">重置</el-button>
      </el-form-item>
    </el-form>
    <router-link :to="'/account/login'" class="tologin">已有帐号？去登陆</router-link>
  </div>
</template>

<script>
  import util from '../utils/util.js'
  import login from './login.vue'
  export default {
    data() {
      var validateuser = (rule, value, callback) => {
        // console.log(value, /^\d{11}$/.test(value))
        if (value === '') {
          callback(new Error('请输入用户名'));
        } else if (!/^\w{6,12}$/.test(value)) {
          callback(new Error('请输入11位手机号'));
        } else {
          callback()
        }
      };
      var validatepass = (rule, value, callback) => {
        // console.log(value, /^.{6,12}$/.test(value))
        if (value === '') {
          callback(new Error('请输入密码'));
        } else if (!/^.{6,12}$/.test(value)) {
          callback(new Error('密码必须是6-12位'));
        } else {
          callback()
        }

      };

      var validatepass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm2.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };

      var validateemail = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入邮箱'));
        } else if (!/^[\w$%?-]+@(\w+)(\.\w+)*$/.test(value)) {
          callback(new Error('请输入正确邮箱格式'));
        } else {
          callback()
        }
      };

      var validatecaptcha = (rule, value, callback) => {
        // console.log(value, /^[a-zA-Z0-9]{4}$/.test(value))
        if (value === '') {
          callback(new Error('请输入验证码'));
        } else if (!/^[a-zA-Z0-9]{4}$/.test(value)) {
          callback(new Error('验证码必须是4位数字与字母'));
        } else {
          callback()
        }

      };
      return {
        height: '550px',
        captcha_url: "",
        uuid: "",
        ruleForm2: {
          user: '',
          pass: '',
          pass2: '',
          captcha: '',
          email: '',

        },
        rules2: {
          user: [{
            validator: validateuser,
            trigger: 'blur'
          }],
          pass: [{
            validator: validatepass,
            trigger: 'blur'
          }],
          pass2: [{
            validator: validatepass2,
            trigger: 'blur'
          }],
          captcha: [{
            validator: validatecaptcha,
            trigger: 'blur'
          }],
          email: [{
            validator: validateemail,
            trigger: 'blur'
          }],
        }
      };
    },
    mounted() {
      this.generate_captcha();
      var box = document.getElementsByClassName('login')[0];
      box.style.height = '550px';
    },
    methods: {
      generate_captcha() {
        this.uuid = util.generate_uuid()
        this.captcha_url = this.host + '/captcha/' + this.uuid + "/";
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.axios.post(this.host + "/register/", {
              username: this.ruleForm2.user,
              password: this.ruleForm2.pass,
              captcha: this.ruleForm2.captcha,
              email: this.ruleForm2.email,
              uuid: this.uuid
            }, {
              responseType: 'json',
              withCredentials: true,
            }).then(response => {
              // 使用浏览器本地存储保存token
              // 未记住登录
              console.log(response, "response")
              localStorage.clear();
              sessionStorage.token = response.data.token;
              sessionStorage.user_id = response.data.user_id;
              sessionStorage.username = response.data.username;
              this.$router.push({
                name: 'info'
              })

            }).catch(error => {
              console.log(error.response.data, "error")
              this.$message({
                type: 'error',
                message: error.response.data.msg + ',注册失败!'
              });
            });


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

<style>
  .tologin{
    color: #8A82DB;
    float: right;
    margin: 20px;

  }
  .tologin:hover{
    text-decoration: underline;

  }
  .el-form {
    width: 400px;
    height: 300px;
    margin: 50px auto 35px auto;
    font-size: 16px;

  }

  .el-button img {
    width: 80px;

  }
</style>
