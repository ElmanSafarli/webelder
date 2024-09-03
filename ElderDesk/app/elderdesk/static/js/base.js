$(document).ready(function () {
  $(".top-navigation-dropdown-toggle").click(function () {
    $(this).next(".top-navigation-dropdown-content").slideToggle();
  });

  var $nav = $(".bottom-navigation");

  if ($nav.length > 0) {
    var offsetTop = $nav.offset().top;

    $(window).scroll(function () {
      if ($(window).scrollTop() > offsetTop) {
        $nav.addClass("fixed");
      } else {
        $nav.removeClass("fixed");
      }
    });
  }
});
