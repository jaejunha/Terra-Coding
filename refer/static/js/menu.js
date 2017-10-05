function terra_menu(no){
  $('#info').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != '1')
        $(this).css('color','#cccccc');
    }
  )
  $('#coding').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != '2')
        $(this).css('color','#cccccc');
    }
  )
  $('#statistics').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != '3')
        $(this).css('color','#cccccc');
    }
  )
  $('#rank').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != '4')
        $(this).css('color','#cccccc');
    }
  )
  if(no == 1){
    loadDiv('/info');
    $('#info').css('color','#aaaaaa');
    $('#coding').css('color','#cccccc');
    $('#statistics').css('color','#cccccc');
    $('#rank').css('color','#cccccc');
    $('#selector').css('left',$('#info').offset().left+'px');
    $('#selector').css('width',$('#info').width()+'px');
  }else if(no == 2){
    loadDiv('/coding');
    $('#info').css('color','#cccccc');
    $('#coding').css('color','#aaaaaa');
    $('#statistics').css('color','#cccccc');
    $('#rank').css('color','#cccccc');
    $('#selector').css('left',$('#coding').offset().left+'px');
    $('#selector').css('width',$('#coding').width()+'px');
  }else if(no == 3){
    loadDiv('/statistics');
    $('#info').css('color','#cccccc');
    $('#coding').css('color','#cccccc');
    $('#statistics').css('color','#aaaaaa');
    $('#rank').css('color','#cccccc');
    $('#selector').css('left',$('#statistics').offset().left+'px');
    $('#selector').css('width',$('#statistics').width()+'px');
  }else if(no == 4){
    loadDiv('/rank');
    $('#info').css('color','#cccccc');
    $('#coding').css('color','#cccccc');
    $('#statistics').css('color','#cccccc');
    $('#rank').css('color','#aaaaaa');
    $('#selector').css('left',$('#rank').offset().left+'px');
    $('#selector').css('width',$('#rank').width()+'px');
  }
}
