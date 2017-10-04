function login_ani_timeout(){
  var loopTimer = window.setTimeout(function(){
    var simple = $('#simple');

    simple.css('border-radius','0%');
    simple.css('width','5%');
    simple.css('height','5%');
    simple.css('position','relative');
    simple.css('transform-origin','0% 0%');
    simple.css('left','0px');
    simple.css('top','0px');
    simple.css('overflow-x','hidden');
    simple.css('overflow-y','hidden');
    simple.css('background','linear-gradient(#5a92b7, #6cc1a0 ) fixed');
    simple.css('z-index','-2');
  }, 3000);
}
