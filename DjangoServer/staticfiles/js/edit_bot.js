$(document).ready(function() {
    $(".btn-ghost-primary").filter(function() {
        return $(this).data("target") === "#bot_settings";
      }).click(function(e) {
      e.preventDefault();
      var icon = $(this).find("i");
      if (icon.hasClass("fa-arrow-down")) {
        icon.removeClass("fa-arrow-down").addClass("fa-arrow-up");
      } else {
        icon.removeClass("fa-arrow-up").addClass("fa-arrow-down");
      }
      $("#bot_settings").toggleClass('collapse');
    });
  });