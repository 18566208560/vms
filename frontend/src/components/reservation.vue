<template>
	<div class="reservation">
	<el-row>
		<el-col :span="24" class="p_title">

			<el-row>
        <el-col :span="6"><span :span="6" class="title">预约实验</span></el-col>
				<el-col :span="6"><span class="rackname">{{rackname}}</span></el-col>
				<el-col :span="6"><span>{{c_date}}</span></el-col>
<!-- 				<el-col :span="4"><span>已预约时间段<b>{{}}</b></span></el-col>
				<el-col :span="4"><span>剩余约时间段<b>{{}}</b></span></el-col> -->
			</el-row>

		</el-col>
	</el-row>

	<el-row>
		<el-col :span="4"  class="date">

			  <el-button plain :type="c_date==date2str(date,i-1)?'primary':'info'" @click="get_reservation(rackid,date2str(date,i-1))" v-for="i in days">
			  {{date|addate(i-1)|format("yyyy-MM-dd")}}
			  </el-button>

		</el-col>

		<el-col :span="20" class="con">


			<el-card class="box-card" v-for="lab in infos"  shadow="hover">
			  <div slot="header" class="clearfix">
				<span>{{lab.lab_name}}</span>
				<!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
			  </div>
			  <div class="text item">
				  <div v-for="it in lab.tb_list" class="badge">
					<el-tooltip class="item" effect="dark" :content="it.user.join(' | ')" placement="top">
						<el-badge :value="it.count" class="item">
							<el-button type="success" v-on:click="sub_rv(it.id+'/'+it.tb,lab.lab_name)" :disabled="due(it.tb) && it.count>0?false:true">
							{{it.tb}}
							</el-button>
						</el-badge>
					</el-tooltip>
				  </div>

			  </div>
			</el-card>
        <div v-if="!infos.length" style="text-align: center;margin:30px;color:#999;">
        暂无数据!
    </div>




		</el-col>
	</el-row>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				userid:sessionStorage.user_id || localStorage.user_id,
				username:sessionStorage.username || localStorage.username,
				token:sessionStorage.token || localStorage.token,
				lablist:[], //指定rack的 所有实验基础数据
				reservation_list:[],  //指定日期的 预约实验数据
				rackid:"",     //rack id
				rackname:"",   //rack name 通过watch 监听 url query 获取
				c_date:"",  // 当前 日期
				days:7,  //可预约天数
				date:new Date(),
			}
		},
		watch:{
		      '$route.query':function(newVal,oldVal){ // 监听url query 部分 更改rack信息 并重新请求lab数据
				  console.log(newVal,oldVal)
				this.rackid = newVal.rackid;
				this.rackname = newVal.rackname;
				this.getlab(this.rackid);
				this.get_reservation(this.rackid,this.c_date)
		      },
			},
		computed:{
			infos:function(){   // 数据请教的lab两条数据  拼接为新数据 进行遍历
				var c_data = []
				for (var data of this.lablist){
					var tb_list=[]
					for (var tb in data.lab_tb){
						var user=[]
						for (var rs of this.reservation_list){
							if (data.lab_name == rs.lab && tb == rs.tb_id.split("/")[0]){
								user.push(rs.user)
							}
						}
						var count = data.count-user.length
						tb_list.push({"id":tb,"tb":data.lab_tb[tb],"user":user,"count":count})
					}
					c_data.push({
					"tb_list":tb_list,
					"lab_name":data.lab_name,
					"count":data.count,
					})
				}
				console.log(c_data)
				return c_data
			},

// 			reserved:function(){var j=0;for(var i of this.info){if(i.userid){j+=1}};return j;},
// 			remanent:function(){return 16-this.reserved},
		},
		mounted(){
			// this.get_info(this.date);
			// 页面加载 更新rack数据  并重新请求lab数据  在计算属性里面进行拼接
			this.rackid = this.$route.query.rackid
			this.rackname = this.$route.query.rackname
			this.c_date = this.date2str(this.date)
			console.log(this.$route.query.rackid,"********************")
			this.getlab(this.rackid); //指定rack的 所有实验基础数据
			this.get_reservation(this.rackid,this.c_date); //指定日期的  所有实验基础数据
		},
		methods:{

			getlab:function(rackid){  //指定rack  所有实验基础数据
				this.axios.get(this.host+'/getlab/'+rackid+"/",
					{responseType:'json',
					headers: {'Authorization': 'JWT ' + this.token},
					withCredentials: true,    //跨域带上cookies
					},
					).then(response=>{
						console.log(response,this)
						this.lablist = response.data
					}).catch(error=>{
						console.log(error.response.data);
					})
			},
			get_reservation:function(rackid,date){  //指定日期  预约实验数据
				this.axios.get(this.host+'/reservation/'+rackid+"/"+date+"/",
						// http://127.0.0.1:8000/getreservation/1/2019-09-12/
						{responseType:'json',
						headers: {'Authorization': 'JWT ' + this.token},
						withCredentials: true,    //跨域带上cookies
						},
						).then(response=>{
							console.log(response,this)
							this.reservation_list = response.data
							this.c_date=date     // 请求成功 更新当前日期
						}).catch(error=>{
							console.log(error.data);
						})
			},

			due:function(tb){
				// 判断 时段开始时间是否大于当前时间  若大于 则不可操作
				var tb_t = Date.parse(this.c_date+" "+tb.split("-")[0])
				if (new Date().getTime()<tb_t-1000*60*1){
					return true
				}else{
					return false
				}
			},

			// 项目中没有用到 ，使用mounted中用 this.$route.query.rackid代替
			get_query_string: function(name){ // name = "next"  获取 url 查询参数
				var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');   //'(^|&)next=([^$]*)(&|$)'
				// window.location.search 获取地址栏上面的查询字符串

				var r = window.location.search.substr(1).match(reg);
				if (r != null) {

					return decodeURI(r[2]);
				}
				return null;
			},
			// 项目中没有用到 ，使用mounted中用 this.$route.query.rackid代替
			get_query_string2:function(name){  //获取 url 查询参数
				var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');   //'(^|&)next=([^$]*)(&|$)'
				var r = window.location.href.split("?")[1].match(reg);
				if (r != null) {

				    return decodeURI(r[2]);
				}
				return null;


			},

			get_info:function(date){
		    let rock = this.$route.query.rock;
			  var d = this.date2str(date);
			  this.old_info=[
			    {"date":d,"tb_id":1,"time_bucket":"00:00-06:00"},
				{"date":d,"tb_id":2,"time_bucket":"06:30-10:30"},
				{"date":d,"tb_id":3,"time_bucket":"11:00-15:00"},
				{"date":d,"tb_id":4,"time_bucket":"15:30-19:30"},
				{"date":d,"tb_id":5,"time_bucket":"20:00-24:00"}];

				this.axios.get(this.host+'/get_info/?rock='+rock+'&date='+this.date2str(date),
				{responseType:'json',
				headers: {'Authorization': 'JWT ' + this.token},
				withCredentials: true,    //跨域带上cookies
				},
				).then(response=>{
					// console.log(response.data);
					// console.log(this.old_info);
          this.info = this.merge_data(response.data);
            // console.log(this.merge_data(response.data))
				}).catch(error=>{
					console.log(error.response.data);
				})
			},
			merge_data:function(data){
				if(data!=''){
				  for(var i=0;i<data.length;i++){
					for(var j=0;j < 5;j++){
					  if (data[i].tb_id === this.old_info[j].tb_id){
						this.old_info[j] = data[i]
					  }
				  }
				}
				  return this.old_info
				}else{return this.old_info}


			  },
			sub_rv:function(tb_id,lab_name){
				// 提交预约
				// 弹窗确认
				this.$confirm('确定预约, 是否继续?', '提示', {
				  confirmButtonText: '确定',
				  cancelButtonText: '取消',
				  type: 'warning'
				}).then(() => {
					console.log("xxxx",this.c_date,tb_id,this.userid,this.rackid,lab_name)
					this.axios.post(this.host+'/reservation/',
					{date:this.c_date,tb_id:tb_id,userid:this.userid,rackid:this.rackid,labname:lab_name},
					{responseType:'json',
					headers: {'Authorization': 'JWT ' + this.token},
					withCredentials: true,    //跨域带上cookies
					}
					).then(response=>{
					  console.log(response.data);
						if (response.data.status="ok"){
							this.get_reservation(this.rackid,this.c_date)
							this.$message({
								type: 'success',
								message: response.data.msg
							});
						}else{
							this.$message({
								type: 'error',
								message: response.data.msg
							});
						}

					}).catch(error=>{
					  console.log(error);
						this.$message({
							type: 'error',
							message: '预约失败!'+error.data.msg
						});
					});

				}).catch(() => {
				  this.$message({
					type: 'info',
					message: '已取消xxx预约'
				  });

				});


			},
			// 日期转字符 串， 第二个参数 为日期加或减指定 天数
			date2str:function(date,day=0){
				// 日期转字符串
				var date = new Date(date.getTime() + 24 * 60 * 60 * 1000 * day)
				var month = date.getMonth()+1
				return date.getFullYear()+"-"+month+"-"+date.getDate()
			},


		},
		// 日期格式化过滤器
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
			},
			// 日期加减过滤器
			addate:function(date,num){
				return new Date(date.getTime() + 24 * 60 * 60 * 1000 * num)
			},
		}
	}
</script>

<style>

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

	.el-card{
		margin: 10px;
	}
	.el-card .badge{
		display: inline-block;
		margin-right: 20px;
	}




</style>
