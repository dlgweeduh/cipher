
$(document).ready(function() {
    var windowH = $(window).height();
    var wrapperH = $('.hero').height();
    if(windowH > wrapperH) {                            
        $('.hero').css({'height':($(window).height())+'px'});
    }                                                                               
    $(window).resize(function(){
        var windowH = $(window).height();
        var wrapperH = $('.hero').height();
        var differenceH = windowH - wrapperH;
        var newH = wrapperH + differenceH;
        var truecontentH = $('.heroContent').height();
        if(windowH > truecontentH) {
            $('.hero').css('height', (newH)+'px');
        }

    })          
});