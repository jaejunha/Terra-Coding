function terra_menu(no){
  $('#info').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != 1)
        $(this).css('color','#cccccc');
      else
        $(this).css('color','#aaaaaa');
    }
  )
  $('#coding').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != 2)
        $(this).css('color','#cccccc');
      else
        $(this).css('color','#aaaaaa');
    }
  )
  $('#vdb').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != 3)
        $(this).css('color','#cccccc');
      else
        $(this).css('color','#aaaaaa');
    }
  )
  $('#feedback').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != 4)
        $(this).css('color','#cccccc');
      else
        $(this).css('color','#aaaaaa');
    }
  )
  if(no == 1){
    loadDiv('/info');
    $('#info').css('color','#aaaaaa');
    $('#coding').css('color','#cccccc');
    $('#vdb').css('color','#cccccc');
    $('#feedback').css('color','#cccccc');
    $('#selector').css('left',$('#info').offset().left+'px');
    $('#selector').css('width',$('#info').width()+'px');
  }else if(no == 2){
    $("#dialog_coding").dialog({
      autoOpen: true,
      modal:	true,
      disabled:	true
    });
  }else if(no == 3){
    loadDiv('/vdb');
    $('#info').css('color','#cccccc');
    $('#coding').css('color','#cccccc');
    $('#vdb').css('color','#aaaaaa');
    $('#feedback').css('color','#cccccc');
    $('#selector').css('left',$('#vdb').offset().left+'px');
    $('#selector').css('width',$('#vdb').width()+'px');
  }else if(no == 4){
    loadDiv('/feedback');
    $('#info').css('color','#cccccc');
    $('#coding').css('color','#cccccc');
    $('#vdb').css('color','#cccccc');
    $('#feedback').css('color','#aaaaaa');
    $('#selector').css('left',$('#feedback').offset().left+'px');
    $('#selector').css('width',$('#feedback').width()+'px');
  }
}

function admin_menu(no){
  $('#info').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != 1)
        $(this).css('color','#cccccc');
      else
        $(this).css('color','#aaaaaa');
    }
  )
  $('#problem').hover(
    function(){
      $(this).css('color','#aaaaaa');
    },
    function(){
      if(no != 2)
        $(this).css('color','#cccccc');
      else
        $(this).css('color','#aaaaaa');
    }
  )
  if(no == 1){
    loadDiv('/info');
    $('#info').css('color','#aaaaaa');
    $('#problem').css('color','#cccccc');
    $('#selector').css('left',$('#info').offset().left+'px');
    $('#selector').css('width',$('#info').width()+'px');
  }else if(no == 2){
    loadDiv('/problem');
    $('#info').css('color','#cccccc');
    $('#problem').css('color','#aaaaaa');
    $('#selector').css('left',$('#problem').offset().left+'px');
    $('#selector').css('width',$('#problem').width()+'px');
  }
}
