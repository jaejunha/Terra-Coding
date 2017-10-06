function intro_timeout(){
  setTimeout(function() {
    $('#gradation').css('animation','disappear 2s');
    $('#gradation').css('animation-fill-mode','both');
    $('#developer').css('animation','disappear2 2s');
    $('#developer').css('animation-fill-mode','both');
  }, 1000);

  setTimeout(function() {
     $('#logo').css('animation','appear 3s');
     $('#logo').css('animation-fill-mode','both');
     $('#logo').css('animation-iteration-count','infinite');
     $('#copy').css('opacity','1');
  }, 3000);
}
