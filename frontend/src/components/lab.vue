<template>
	        <div id="display"></div>

</template>

<script>
	import Guacamole from '../utils/all.js'
	export default {
		data(){
			return{
				
			};
		},
		mounted() {
// 			const oScript = document.createElement('script');
// 			oScript.type = 'text/javascript';
// 			oScript.src = '/utils/all.min.js';
// 			document.body.appendChild(oScript);
		}
		methods:{
			connect(){
				 // Get display div from document
				var display = document.getElementById("display");
				
				// Instantiate client, using an HTTP tunnel for communications.
				var guac = new Guacamole.Client(
				    new Guacamole.HTTPTunnel("tunnel")
				);
				
				// Add client to display div
				display.appendChild(guac.getDisplay().getElement());
				
				// Error handler
				guac.onerror = function(error) {
				    alert(error);
				};
				
				// Connect
				guac.connect();
				
				// Disconnect on close
				window.onunload = function() {
				    guac.disconnect();
				}
				
				// Mouse
				var mouse = new Guacamole.Mouse(guac.getDisplay().getElement());
				
				mouse.onmousedown = 
				mouse.onmouseup   =
				mouse.onmousemove = function(mouseState) {
				    guac.sendMouseState(mouseState);
				};
				
				// Keyboard
				var keyboard = new Guacamole.Keyboard(document);
				
				keyboard.onkeydown = function (keysym) {
				    guac.sendKeyEvent(1, keysym);
				};
				
				keyboard.onkeyup = function (keysym) {
				    guac.sendKeyEvent(0, keysym);
				};
			},
		},
	}
	
           

</script>

<style>
</style>
