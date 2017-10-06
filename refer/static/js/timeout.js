function intro_timeout(){
  setTimeout(function() {
    $('#gradation').css('animation','disappear 2s');
    $('#gradation').css('animation-fill-mode','both');
  }, 1000);

  setTimeout(function() {
     $('#developer').css('opacity','0');
     $('#logo').css('animation','appear 3s');
     $('#logo').css('animation-fill-mode','both');
     $('#logo').css('animation-iteration-count','infinite');
     $('#copy').css('opacity','1');
  }, 2000);
}
