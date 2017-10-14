function index_intro(){
  $('#screen').css('position','absolute');
  $('#screen').css('left','0px');
  $('#screen').css('top','0px');
  $('#screen').css('width','100%');
  $('#screen').css('height','100%');
  $('#screen').css('background','#000000');
  $('#screen').css('animation','screen 1s');
  $('#screen').css('animation-fill-mode','both');
  $('#screen').css('z-index','2');

  $('#header').css('-webkit-animation-delay','2s');
  $('#header').css('animation','header 1.5s');
  $('#header').css('animation-fill-mode','both');

  $('#title').css('animation','title 2.5s');
  $('#title').css('animation-fill-mode','both');

  $('#top').css('top','-80px');
  $('#top').css('animation','top 2.5s');
  $('#top').css('animation-fill-mode','both');

  $('#content').css('animation','content 2.5s');
  $('#content').css('animation-fill-mode','both');
}
