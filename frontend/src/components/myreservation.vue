<template>
	<div class="reservation">
    <el-row>
		<el-col :span="24" class="p_title">
      <span class="title">已预约面试</span>
			<span>面试已预约时间段：<b>{{num1}}</b></span>
		</el-col>
	</el-row>
	<el-table
    :data="interview"
    style="width: 100%"
    :row-class-name="tableRowClassName">
    <el-table-column
      prop="date"
      label="日期"
      width="180"
    style="border-left: 20px">
    </el-table-column>
    <el-table-column
      prop="time_bucket"
      label="时段"
      width="180">
    </el-table-column>
    <el-table-column
      prop="count"
      label="面试人数">
    </el-table-column>
    <el-table-column
      prop="msg"
      label="备注">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="取消预约"
      width="120">
      <template slot-scope="scope">
        <!-- @click.native.prevent="deleteRow(scope.$index, tableData)"-->
        <el-button
          v-on:click="sub_in(scope.row.date,scope.row.tb_id)"
          type="text"
          size="small">
          取消
        </el-button>
      </template>
    </el-table-column>
  </el-table>
    <br>
	<el-row>
		<el-col :span="24" class="p_title">
      <span class="title">已预约实验</span>
			<span>实验已预约时间段：<b>{{num2}}</b></span>
		</el-col>
	</el-row>
	<el-row class="myrev">
		<el-collapse v-model="activeNames" >

		  <el-collapse-item :title="index" :name="index" v-for="(it,index) in reservation">
			<el-row class="con_con">

				<el-col :span=6 v-for="(tb,inx) in it">
					<el-badge value="已预约" class="item" >
						<el-button type="success" v-on:click="sub_rv(index,inx)" v-if="test(index,tb.tb_id)" :disabled="due(index,tb.tb_id)">
						{{tb.rack}}<br/>{{tb.lab}}<br/>{{tb.tb_id.split("/")[1]}}
						</el-button>
						<el-button  v-else>
						  <span v-on:click="to_lab(index,inx)">{{tb.rack}}<br/>{{tb.lab}}<br/>{{tb.tb_id.split("/")[1]}}<br/>进入实验</span>
						</el-button>
					</el-badge>
				</el-col>

			</el-row>
		  </el-collapse-item>
      <div v-if="!show_reservation" style="text-align: center;margin:30px;color:#999;">
        暂无数据!
    </div>
		</el-collapse>
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
				activeNames:"",  //展开信息序号
				reservation:[],
				interview:[],
			}
		},
		computed:{
			//已预约时间段数量
      num1:function(){
						return this.interview.length;
					},
			num2:function(){
        var num= 0
        for (var i in this.reservation) {
          num += this.reservation[i].length
        }
         return num
			},
      show_reservation:function(){
        return Object.keys(this.reservation).length
      }

		},
		mounted(){
			this.get_reservation();
			this.get_info(this.date);
		},
		methods:{
			 tableRowClassName({row, rowIndex}) {
				if (rowIndex%2 === 1) {
				  return 'warning-row';
				}
				return '';
			  },

      get_info:function(){
				// 获取 面试预约信息
				this.axios.get(this.host+'/myinterview/',
				{responseType:'json',
				headers: {'Authorization': 'JWT ' + this.token},
				withCredentials: true,    //跨域带上cookies
				},
				).then(response=>{
					this.interview = response.data
				}).catch(error=>{
					console.log(error.response.data);
				})
			},
      sub_in:function(date,tb_id){
				// 取消面试预约
				// 弹窗确认
				this.$confirm('取消预约, 是否继续?', '提示', {
				  confirmButtonText: '确定',
				  cancelButtonText: '取消',
				  type: 'warning'
				}).then(() => {
					this.axios.post(this.host+'/myinterview/',
          {"date":date,"tb_id":tb_id},
					{responseType:'json',
					headers: {'Authorization': 'JWT ' + this.token},
					withCredentials: true    //跨域带上cookies
					},
					).then(response=>{
						if (response.data.status === "ok"){
							this.get_info();
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
						this.$message({
							type: 'error',
							message: '取消预约失败!'
						});
					})
				}).catch(() => {
				  this.$message({
					type: 'info',
					message: '取消预约'
				  });
				});

			},
			get_reservation(){
				// 获取 实验预约信息
					this.axios.get(this.host+'/myreservations/'+ this.userid+"/",
					{responseType:'json',
					headers: {'Authorization': 'JWT ' + this.token},
					withCredentials: true,    //跨域带上cookies
					},
					).then(response=>{
					  console.log(response.data);
						this.reservation = response.data;
					}).catch(error=>{
						console.log(error.response.data);
					})
				},


			sub_rv:function(index,idx){
				// 取消实验预约
				// 弹窗确认
				this.$confirm('取消预约, 是否继续?', '提示', {
				  confirmButtonText: '确定',
				  cancelButtonText: '取消',
				  type: 'warning'
				}).then(() => {
					this.axios.post(this.host+'/myreservations/',
					this.reservation[index][idx],
					{responseType:'json',
					headers: {'Authorization': 'JWT ' + this.token},
					withCredentials: true    //跨域带上cookies
					},
					).then(response=>{
						if (response.data.status == "ok"){
							this.get_reservation();
							this.$message({
								type: 'success',
								message: response.data.msg
							});
						}else{
							this.$message({
								type: 'success',
								message: response.data.msg
							});
						}
					}).catch(error=>{
						this.$message({
							type: 'error',
							message: '取消预约失败!'
						});
					})
				}).catch(() => {
				  this.$message({
					type: 'info',
					message: '取消预约'
				  });
				});

			},
			test(date,tb){
				// 判断 是否在实验 时间范围内
				var tb_start = Date.parse(date+" "+tb.split("/")[1].split("-")[0])
				var tb_end = Date.parse(date+" "+tb.split("/")[1].split("-")[1])
					console.log(tb_start,new Date().getTime(),tb_start<new Date().getTime() && new Date().getTime()<tb_end)
					if (tb_start<new Date().getTime() && new Date().getTime()<tb_end){
						return false
					}else{
						return true
					}
			},
			due:function(date,tb){
				// 判断 时段开始时间是否大于当前时间  若大于 则不可操作
				var tb_t = Date.parse(date+" "+tb.split("/")[1].split("-")[0])
				console.log(new Date().getTime(),tb_t-1000*60*5)
				if (new Date().getTime()>tb_t-1000*60*5){
					return true
				}else{
					return false
				}
			},


			to_lab:function(index,idx){
			// 进入实验
			  this.axios.post(this.host + '/experiment/',
				this.reservation[index][idx],
				{responseType:'json',
				headers: {'Authorization': 'JWT ' + this.token},
				withCredentials: true    //跨域带上cookies
				}).then(response=>{
					if (response.data.status=="ok"){
						this.$message({
							type: 'success',
							message: response.data.msg
						})
						localStorage.GUAC_AUTH = response.data.data
						// 计算实验时长
						var info = this.reservation[index][idx]
						var tb_list = info.tb_id.split("/")[1].split("-")
						var tb_start = new Date().getTime()
						var tb_end = Date.parse(info.date+" "+tb_list[1])
						var interval = (tb_end-tb_start)/1000
						console.log(tb_end-tb_start,"------------")
						// 定时实验时长的时间  清除localStorage中的guacamole的token
						setTimeout(function () {
							localStorage.clear()
							}, interval);
						// 跳转
						window.open(this.host.replace("api","remote")+"/","_blank")
						// location.href = response.data.url
					}else{
						this.$message({
							type: 'error',
							message: response.data.msg
						})
					}
				}).catch(error=>{
				  this.$message({
				  	type: 'error',
				  	message: "进入实验失败"
				  })
				})
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


	.myrev{
		border: 1px solid #DCDFE6;
		background-color: #fff;
		border-radius:6px;
		overflow: hidden;
	}
	.myrev .el-collapse-item{
		padding:0 20px;
	}

	.myrev .el-collapse-item__header{
		font-size:20px;
		padding-left: 20px;
	}

	.con_con .el-col{
		margin: 15px 0;
		text-align: center;
	}
	.con_con .el-col .el-button{
		width:150px;
	}
	.el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }


</style>

