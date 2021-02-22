function addEv()
{
$(function(){
  $('.minimizedNew').click(function(event) {
    var i_path = $(this).attr('maximize');
    if ($(this).attr("src") == $(this).attr("minim"))
        {
            $(this).attr('src', $(this).attr('gifi'));
            $(this).attr('class', 'minimized');
        }

    else if ($(this).attr("src") == $(this).attr("gifi"))
        {
        $(this).attr('src', $(this).attr('minim'));
        $(this).attr('class', 'minimized');
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

}


setInterval(function () {
    $.ajax({
        type: "post",
        url: "/getT?ts="+currentTS,
        data: $('#ajaxForm').serialize(),
        success: function(data) {

            currentTS = data.result.currTS;
            //console.log(data);
            if( data.result.len > 0)
            {
                arr = data.result.rez;
                arr.forEach(function(item, i, arr)
                {
                    lastHour = document.getElementById("lastHour").textContent.trim();
                    if (lastHour == item[4])
                    {
                    }
                    else
                    {
                        var output  = '<div class="title" id="lastHour">'+item[4]+'</div>';
                        var output2 = '<div id="lastList" class="info">';
                        document.getElementById("lastList").id = 'aaaaa';
                        document.getElementById("lastDay").insertAdjacentHTML('afterbegin',output2);
                        document.getElementById("lastHour").id = 'aaaa';
                        document.getElementById("lastDay").insertAdjacentHTML('afterbegin',output);
                    }
                    var output='<img class="minimizedNew" src="/img/'+ item[0]+'" '
                     +' maximize="/img/'+ item[1]+'" '
                     +' minim="/img/'+ item[0]+'" '
                     +' gifi="/img/'+ item[2]+'"> ';
                    document.getElementById("lastList").insertAdjacentHTML('afterbegin',output);
                    console.log('added!');
                    addEv();






                });


            }
        }
    });
}, 3000);