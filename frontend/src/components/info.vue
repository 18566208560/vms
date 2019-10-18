<template>
	<el-container class="container">
	  <el-header>
      <el-row class="info_header">
        <el-col :span="20"><img src="../assets/Yeslab_logo.png" alt="yeslab_logo"></el-col>
        <el-col :span="2"><span>{{username}}</span></el-col>
        <el-col :span="2"><el-button type="info" v-on:click="logout()">退出</el-button></el-col>
      </el-row>
	  </el-header>
	  <el-container style="min-height: 600px;">


<el-row style="width: 300px; background-color: rgb(84, 92, 100);">
  <el-col :span="24">
    <el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      background-color="#545c64"
      text-color="#fff"
      router=true
      active-text-color="#ffd04b">
      <el-menu-item index="/info/userinfo">
        <i class="el-icon-user"></i>
        <span slot="title">用户中心</span>
      </el-menu-item>

      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-phone-outline"></i>
          <span>预约实验</span>
        </template>
        <el-menu-item :index="'/info/reservation/?rackid='+rack.id+'&rackname='+rack.rack_name" v-for="rack in racklist">
								<span style="padding-left: 30px;">{{rack.rack_name}}</span>
        </el-menu-item>

       </el-submenu>



      <el-menu-item index="/info/interview">
        <i class="el-icon-alarm-clock"></i>
        <span slot="title">预约面试</span>
      </el-menu-item>

      <el-menu-item index="/info/myreservation">
        <i class="el-icon-s-custom"></i>
        <span slot="title">我的预约</span>
      </el-menu-item>
    </el-menu>
  </el-col>
</el-row>



		<el-main>
			 <router-view></router-view>
		</el-main>
	  </el-container>
	</el-container>
</template>

<script>
  import login from './login.vue'
  import reservation from './reservation.vue'
	export default {
	  data() {
	    return {
			isactive:true,
		    userid:sessionStorage.user_id || localStorage.user_id,
		    username:sessionStorage.username || localStorage.username,
		    token:sessionStorage.token || localStorage.token,
			racklist:[],
	  }
	  },

    mounted(){

	    if(!this.token){
	      this.$router.push({name: 'account'})
		}

		this.getrack()

    },
	  methods: {
	    handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
		goreservation(num) {
        // this.$router.push({path:'/info/reservation',query: {rock: num }})
		},
		onSubmit() {
	      console.log('submit!');
	    },
    logout(){
		  this.$confirm('退出登陆, 是否继续?', '提示', {
				  confirmButtonText: '确定',
				  cancelButtonText: '取消',
				  type: 'warning'
				}).then(() => {
				      localStorage.clear();
              sessionStorage.clear();
			        this.$router.push({name:'account'})
      }).catch(error=>{
        this.$message({
					type: 'info',
					message: '取消退出'
				  });
      });
    },
		getrack(){
			this.axios.get(this.host+'/getrack/',
				{responseType:'json',
				headers: {'Authorization': 'JWT ' + this.token},
				withCredentials: true,    //跨域带上cookies
				},
				).then(response=>{
					console.log(response,this)
					this.racklist = response.data
				}).catch(error=>{
					console.log(error.response.data);
				})
		},
	  },
	}

</script>
<style>
  	.p_title{
		color:#999;
		height: 50px;
		line-height: 50px;
		border: 1px solid #DCDFE6;
		background-color: #fff;
		border-radius: 6px;
		margin-bottom: 20px;
    box-shadow: #333 5px 5px 20px 1px;
	}
	.p_title .title{
		margin: 0 20px;
	}
</style>
<style scoped>
  li{
    display: block;
  }
.container{

	width:1440px;
	margin:50px auto;
	box-shadow: #333 10px 10px 30px 5px ;

}
.info_header{
  text-align: center;
  height:60px;
  overflow: hidden;
  line-height: 60px;
}

.el-header{

	background-color: #fff;
	padding:0;

}
</style>
