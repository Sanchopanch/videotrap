$(function(){
  $('.minimized').click(function(event) {
    var i_path = $(this).attr('maximize');
    if ($(this).attr("src") == $(this).attr("minim"))
        $(this).attr('src', $(this).attr('gifi'))
    else if ($(this).attr("src") == $(this).attr("gifi"))
        {
        //$(this).attr('src', $(this).attr('minim'));

        $('body').append('<div id="overlay"></div><div id="magnify"><img src="'+i_path+'"><div id="close-popup"><i></i></div></div>');
        $('#magnify').css({
            left: ($(document).width())/2 -300,
            top: ($(window).height())/2-300
            });
        $('#overlay, #magnify').fadeIn('fast');
        }
  });
  
  $('body').on('click', '#close-popup, #overlay', function(event) {
    event.preventDefault();

    $('#overlay, #magnify').fadeOut('fast', function() {
      $('#close-popup, #magnify, #overlay').remove();
    });
  });
});