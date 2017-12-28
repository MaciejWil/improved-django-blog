$(".scroll-down").click(function() {
    $('html,body').animate({
        scrollTop: $(".form-col").offset().top},
        'slow');
});
