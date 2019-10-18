<template>
  <div class="login">
    <router-view></router-view>
  </div>
</template>

<script>
  export default{
  }
</script>

<style>
  .login{
  	width:460px;
  	margin:90px 20%;
  	border:5px solid #ADD8E6;
  	border-radius: 6px;
  	box-shadow: #333 10px 10px 30px 5px;
  	background: -webkit-linear-gradient(#F0F8FF, white, white, #F0F8FF); /* Safari 5.1 - 6.0 */
    background: -o-linear-gradient(#F0F8FF, white, white, #F0F8FF); /* Opera 11.1 - 12.0 */
    background: -moz-linear-gradient(#F0F8FF, white, white, #F0F8FF); /* Firefox 3.6 - 15 */
    background: linear-gradient(#F0F8FF, white, white, #F0F8FF); /* 标准的语法 */
    overflow: hidden;
    transition: 0.3s ease-out;
  }
</style>
