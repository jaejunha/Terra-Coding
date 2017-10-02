function login_init(){
	var screenWidth = window.innerWidth;
	var screenHeight = window.innerHeight;
	var login = document.getElementById('login');
	var width = login.offsetWidth;
	var height = login.offsetHeight;
	var logo = document.getElementById('logo');
	
	login.style.left = (screenWidth-width)/2+'px';
	login.style.top = (screenHeight-height)/2+'px';

	width = logo.offsetWidth;
	logo.style.left = (screenWidth-width)/2+'px';
	logo.style.top = login.offsetTop-height/2+'px';
}

