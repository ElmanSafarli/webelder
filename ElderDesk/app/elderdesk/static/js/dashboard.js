$(document).ready(function () {
  var $searchInput = $(".searchPage-user-input input[type='text']");
  var $defaultBlock = $(".search-default");
  var $resultContent = $(".search-result-content");
  var $organizationContent = $(".search-result-type-content").eq(2);

  function resetSearchResults() {
    $resultContent.children().not($defaultBlock).hide();
    $defaultBlock.show();
  }

  $searchInput.on("input", function () {
    var query = $(this).val().trim();

    if (query.length === 0) {
      resetSearchResults();
      return;
    }

    $defaultBlock.hide();
    $organizationContent.empty();
    $resultContent.children().not($defaultBlock).show();

    $.ajax({
      url: "/dashboard/organizations/get-organizations/",
      method: "GET",
      data: { search: query },
      success: function (response) {
        var organizations = response.organizations;

        if (organizations.length === 0) {
          $organizationContent.append("<p>No organizations found.</p>");
        } else {
          var orgTable = "<table><thead><tr><th>Name</th></tr></thead><tbody>";
          $.each(organizations, function (index, org) {
            orgTable += "<tr><td>" + org.name + "</td></tr>";
          });
          orgTable += "</tbody></table>";

          $organizationContent.append(orgTable);
        }
      },
      error: function () {
        $organizationContent.append("<p>Error retrieving organizations.</p>");
      },
    });
  });

  $(".btn_dashboard").click(function () {
    var target = $(this).attr("id");

    $(".main-content-section").hide();
    $("#" + target + "-section").show();

    $(".left-block nav>div button").removeClass("active");
    $(this).addClass("active");

    localStorage.setItem("activeSection", target);
  });

  var savedSection = localStorage.getItem("activeSection");

  if (savedSection) {
    $(".main-content-section").hide();
    $("#" + savedSection + "-section").show();

    $(".left-block nav>div button").removeClass("active");
    $("#" + savedSection).addClass("active");
  } else {
    $("#views-section").show();
  }

  $("#profile-button").click(function () {
    $("#profile-menu").slideToggle(300);
  });

  $("#add-organization").click(function () {
    $(".shadow-background").fadeIn();
    $(".add-organization-form").fadeIn();
  });

  $(".organization-form-close-btn, .shadow-background").click(function () {
    $(".shadow-background").fadeOut();
    $(".add-organization-form").fadeOut();
  });

  $(".searchPage-filter-menu-dropdown-item-toggle").click(function () {
    $(this)
      .next(".searchPage-filter-menu-dropdown-item-content")
      .slideToggle(200);

    $(this).find("svg").toggleClass("rotate-arrow");
  });

  $(document).click((event) => {
    if (
      !$(event.target).closest("#profile-button").length &&
      !$(event.target).closest("#profile-menu").length
    ) {
      $("#profile-menu").slideUp(300);
    }

    if (
      !$(event.target).closest(".searchPage-filter-menu-dropdown-item").length
    ) {
      $(".searchPage-filter-menu-dropdown-item-content").slideUp(200);
    }

    if (
      !$(event.target).closest(".searchPage-filter-btn").length &&
      !$(event.target).closest(".searchPage-filter-menu").length
    ) {
      $(".searchPage-filter-menu").slideUp(200);
      $(".searchPage-filter-btn").removeClass("box-shadow");
    }

    if (
      !$(event.target).closest(
        "#search-toggle, .dashboard_search section, .dashboard_search-input"
      ).length
    ) {
      $(".dashboard_search section, .dashboard_search-input").removeClass(
        "searchtoggle"
      );
    }
  });

  $("#search-toggle").on("click", function () {
    $(".dashboard_search section").toggleClass("searchtoggle");
    $(".dashboard_search-input").toggleClass("searchtoggle");
  });

  $(".searchPage-filter-btn").click(function () {
    $(this).toggleClass("box-shadow");
    $(".searchPage-filter-menu").slideToggle(200);
  });

  const $inputField = $(".searchPage-user-input input[type='text']");
  const $clearButton = $(
    ".searchPage-user-input button[data-garden-id='clear-user-input']"
  );

  $inputField.on("input", function () {
    $clearButton.toggle(!!$(this).val().length);
  });

  $clearButton.on("click", () => {
    $inputField.val("").trigger("input");
  });

  $("#toggle-organizations-block").on("click", function () {
    $(".views-main-pane").toggleClass("hidden");
    $(".views-pane-organizations").toggleClass("hidden");
    $(".views-pane-organizations-nav").toggleClass("hidden");
  });
});
