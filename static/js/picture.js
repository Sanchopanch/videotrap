$(function(){
  $('.minimized').click(function(event) {
    //var i_path = $(this).attr('maximize');
    $(this).attr('src', $(this).attr('gifi'));
    //$('body').append('<div id="overlay"></div><div id="magnify"><img src="'+i_path+'"><div id="close-popup"><i></i></div></div>');
    //$('#magnify').css({
    // left: ($(document).width())/2,
    // // top: ($(document).height() - $('#magnify').outerHeight())/2 upd: 24.10.2016
     //       top: ($(window).height())/2
  // });
    $('#overlay, #magnify').fadeIn('fast');
  });
  
  $('body').on('click', '#close-popup, #overlay', function(event) {
    event.preventDefault();

    $('#overlay, #magnify').fadeOut('fast', function() {
      $('#close-popup, #magnify, #overlay').remove();
    });
  });
});