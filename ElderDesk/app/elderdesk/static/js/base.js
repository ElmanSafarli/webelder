$(document).ready(function(){
    
    $('.top-navigation-dropdown-toggle').click(function(){
        $(this).next('.top-navigation-dropdown-content').slideToggle();
    });

    var $nav = $('.bottom-navigation');
    
    if ($nav.length > 0) {
        var offsetTop = $nav.offset().top;

        $(window).scroll(function() {
            if ($(window).scrollTop() > offsetTop) {
                $nav.addClass('fixed');
            } else {
                $nav.removeClass('fixed');
            }
        });
    }
     
    $(".btn_dashboard").click(function() {
        var target = $(this).attr('id');
        
        $(".main-content-section").hide();
        $("#" + target + "-section").show();
        
        $('.left-block nav>div button').removeClass('active');
        $(this).addClass('active');
        
        localStorage.setItem('activeSection', target);
    });

    var savedSection = localStorage.getItem('activeSection');
    
    if (savedSection) {
        $(".main-content-section").hide();
        $("#" + savedSection + "-section").show();
        
        $('.left-block nav>div button').removeClass('active');
        $("#" + savedSection).addClass('active');
    } else {
        $("#views-section").show();
    }

    $('#profile-button').click(function() {
        $('#profile-menu').slideToggle(300); 
    });

    $('#add-organization').click(function() {
        $('.shadow-background').fadeIn();
        $('.add-organization-form').fadeIn();
    });

    $('.organization-form-close-btn, .shadow-background').click(function() {
        $('.shadow-background').fadeOut();
        $('.add-organization-form').fadeOut();
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('#profile-button').length && !$(event.target).closest('#profile-menu').length) {
            $('#profile-menu').slideUp(300);
        }
    });
});