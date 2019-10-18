<template>
	<div class="reservation">

    <el-row>
		<el-col :span="24" class="p_title">
			<span class="title">预约面试</span>
		</el-col>
	</el-row>

<div v-for="i in info" class="inter_list">
	<el-row>
		<el-col :span="4"  class="date">
			  <el-button plain v-on:click="get_info(date)" >{{i[0].date}}</el-button>
		</el-col>

		<el-col :span="20" class="con">

			<el-row class="con_con">
				<el-col :span=6 v-for="it in i">
					<el-badge :value="it.remaining?'剩余：'+it.remaining:''" class="item">
						<el-button plain type="success" v-on:click="sub_rv(it.date,it.tb_id)" :disabled="it.remaining==0?true:false">
						{{it.time_bucket}}
						</el-button>
					</el-badge>
          <br/>

            <el-tag v-for="user in it.users" style="margin-right: 3px;">{{user.realname!==""?user.realname:user.username}}</el-tag>


				</el-col>

			</el-row>

		</el-col>

	</el-row>
  </div>
        <div v-if="!info.length" style="text-align: center;margin:30px;color:#999;">
        暂无数据!
    </div>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				userid:sessionStorage.user_id || localStorage.user_id,
				username:sessionStorage.username || localStorage.username,
				token:sessionStorage.token || localStorage.token,
				info:[],
				date:new Date()
			}
		},
		computed:{
			date2:function(){return new Date(this.date.getFullYear(),this.date.getMonth(),this.date.getDate()+1)},
			reserved:function(){var j=0;for(var i of this.info){if(i.userid){j+=1}};return j;},
			remanent:function(){return 16-this.reserved},
		},
		mounted(){
			this.get_info(this.date);
		},
		methods:{
			get_info:function(date){
			  // console.log(date.getMonth()+1)
				// console.log(this.date2str(date));

				this.axios.get(this.host+'/interview_msg/?date='+this.date2str(date),
				{responseType:'json',
				headers: {'Authorization': 'JWT ' + this.token},
				withCredentials: true,    //跨域带上cookies
				},
				).then(response=>{
					console.log(this.userid);
					this.info = response.data
				}).catch(error=>{
					console.log(error.response.data);
				})
			},
			sub_rv:function(date,tb_id){
				// 提交预约
				// 弹窗确认
				this.$confirm('确定预约, 是否继续?', '提示', {
				  confirmButtonText: '确定',
				  cancelButtonText: '取消',
				  type: 'warning'
				}).then(() => {

					this.axios.post(this.host+'/interview/',
					{date:date,tb_id:tb_id,userid:this.userid},
					{responseType:'json',
					headers: {'Authorization': 'JWT ' + this.token},
					withCredentials: true,    //跨域带上cookies
					},
					).then(response=>{
					  console.log(response.data);
					  this.get_info(this.date);
						this.$message({
							type: 'success',
							message: response.data.msg
						});
					}).catch(error=>{

					  console.log(error);
						this.$message({
							type: 'error',
							message: '预约失败!'+error.response.data.msg
						});
					})

				}).catch(() => {
				  this.$message({
					type: 'info',
					message: '已取消预约'
				  });

				});


			},
			date2str:function(date){
				// 日期转字符串
        var month = date.getMonth()+1
				return date.getFullYear()+"-"+month+"-"+date.getDate()
			},
			open1() {
				const h = this.$createElement;

				this.$notify({
				  title: '标题名称',
				  message: h('i', { style: 'color: teal'}, '预约成功！')
				});
      },
		},
		filters:{
			format2:function(date,fmt){
				console.log(date,fmt)
				var o = {
					"M+" : date.getMonth()+1,                 //月份
					"d+" : date.getDate(),                    //日
					"h+" : date.getHours(),                   //小时
					"m+" : date.getMinutes(),                 //分
					"s+" : date.getSeconds(),                 //秒
					"q+" : Math.floor((date.getMonth()+3)/3), //季度
					"S"  : date.getMilliseconds()             //毫秒
				  };
				if(/(y+)/.test(fmt))
					fmt=fmt.replace(RegExp.$1, (date.getFullYear()+"").substr(4 - RegExp.$1.length));
				for(var k in o)
					if(new RegExp("("+ k +")").test(fmt))
				fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
				return fmt;
			}
		}
	}
</script>

<style scoped>

	.reservation{
		background-color: #eee;
	}
	.date .el-button{
		width:80%;
		height:50px;
		margin:10px auto;
		display: block;

	}
	.con{
		background-color: #fff;
		border-radius: 6px;
	}
	.con_title{
		text-align: center;
		height: 50px;
		line-height: 50px;
	}
	.con .el-divider{
		margin:0 0 20px 0;
	}
	.con_con .el-col{
		margin: 15px 0;
		text-align: center;
	}
	.con_con .el-col .el-button{
		width:150px;


	}
  .inter_list{
    margin:10px;
  }
</style>
