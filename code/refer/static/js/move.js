function intro_move(){
		$('#developer').css('left', ($(window).width() - $('#developer').width())/2 +'px' );
		$('#developer').css('top', ($(window).height() - $('#developer').height())/2 +'px' );
		$('#logo').css('left', ($(window).width() - $('#logo').width())/2 +'px' );
		$('#logo').css('top', ($(window).height() - $('#logo').height())/2 +'px' );
		$('#copy').css('top', $('#logo').offset().top + $('#logo').height()+50 +'px' );
}

function login_move(error){
	var screenWidth = window.innerWidth;
	var screenHeight = window.innerHeight;

	if(error == ''){
		var login = document.getElementById('login');
	}else{
		var login = document.getElementById('login_error');
	}
	var width = login.offsetWidth;
	var height = login.offsetHeight;
	var logo = document.getElementById('logo');

	login.style.left = (screenWidth-width)/2+'px';
	login.style.top = (screenHeight-height)/2+'px';

	left= ($(window).width()-$('#logo').width())/2;
	$('#logo').css('left',(left-9)+'px');
	$('#logo').css('top',login.offsetTop-height/2.5+'px');
}

function terra_move(){
	var width = 0.3574*$('#banner').width();
	var height = 0.4314*$('#banner').height();
	$('.simple_banner_wrap').css('width',width);
	$('.simple_banner_wrap').css('height',height);
	$('.simple_banner_wrap ul li').css('background-size',width+'px '+height+'px');

	var left = 0.3096*$('#banner').width();
	var top = 0.1595*$('#banner').height();
	$('.simple_banner_wrap').css('left',left);
	$('.simple_banner_wrap').css('top',top);


	$('.nav_wrap li').css('margin-left','10px');
	$('.nav_wrap li').css('margin-right','10px');
	$('.nav_wrap').css('left',width/2-40);
}
