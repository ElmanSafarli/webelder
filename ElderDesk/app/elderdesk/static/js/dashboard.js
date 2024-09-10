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
      url: "/dashboard/organizations/api/get-organizations/",
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

  function loadOrganizations(page) {
    $.ajax({
      url: "/dashboard/organizations/api/get-organizations/",
      method: "GET",
      data: {
        page: page,
        search: $("#search-input").val(), // Optional: search term if applicable
      },
      success: function (response) {
        var orgCount = response.organizations.length;
        $(".count_organization").text(orgCount + " organizations");

        $("#organization-list tbody").empty();
        $.each(response.organizations, function (index, organization) {
          $("#organization-list tbody").append(`
                    <tr>
                        <td><a href="/dashboard/organizations/${organization.uuid}">${organization.name}</a></td>
                        <td>${organization.domains.join(", ")}</td>
                        <td>${organization.optional_info || "-"}</td>
                        <td><time>${organization.created_date}</time></td>
                    </tr>
                `);
        });

        // Render pagination controls
        updatePaginationControls(response.current_page, response.num_pages);
      },
    });
  }

  // Function to render pagination controls
  function updatePaginationControls(currentPage, numPages) {

    if (numPages <= 1) {
      $("#pagination_organization").hide();  
      return;
    } else {
      $("#pagination_organization").show(); 
    }
  

    let paginationHtml = "";
    let maxPagesToShow = 6;
n
    paginationHtml += `<li data-page="1" ${
      currentPage === 1 ? 'class="disabled"' : ""
    }>
      <svg width="9" height="8" viewBox="0 0 9 8" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4.64645 3.64645C4.45118 3.84171 4.45118 4.15829 4.64645 4.35355L7.82843 7.53553C8.02369 7.7308 8.34027 7.7308 8.53553 7.53553C8.7308 7.34027 8.7308 7.02369 8.53553 6.82843L5.70711 4L8.53553 1.17157C8.7308 0.976311 8.7308 0.659728 8.53553 0.464466C8.34027 0.269204 8.02369 0.269204 7.82843 0.464466L4.64645 3.64645ZM5.0001 3.5H5V4.5H5.0001V3.5Z" fill="#676767" />
        <path d="M0.646446 3.64645C0.451184 3.84171 0.451184 4.15829 0.646446 4.35355L3.82843 7.53553C4.02369 7.7308 4.34027 7.7308 4.53553 7.53553C4.7308 7.34027 4.7308 7.02369 4.53553 6.82843L1.70711 4L4.53553 1.17157C4.7308 0.976311 4.7308 0.659728 4.53553 0.464466C4.34027 0.269204 4.02369 0.269204 3.82843 0.464466L0.646446 3.64645ZM1.0001 3.5H0.999999L0.999999 4.5H1.0001V3.5Z" fill="#676767" />
      </svg>
    </li>`;

    paginationHtml += `<li data-page="${currentPage - 1}" ${
      currentPage === 1 ? 'class="disabled"' : ""
    }>
      <svg width="5" height="8" viewBox="0 0 5 8" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0.646347 3.64645C0.451084 3.84171 0.451084 4.15829 0.646347 4.35355L3.82833 7.53553C4.02359 7.7308 4.34017 7.7308 4.53543 7.53553C4.7307 7.34027 4.7307 7.02369 4.53543 6.82843L1.70701 4L4.53543 1.17157C4.7307 0.976311 4.7307 0.659728 4.53543 0.464466C4.34017 0.269204 4.02359 0.269204 3.82833 0.464466L0.646347 3.64645ZM1 3.5H0.9999L0.9999 4.5H1L1 3.5Z" fill="#676767" />
      </svg>
    </li>`;

    if (currentPage > maxPagesToShow) {
      paginationHtml += `<li>...</li>`;
    }

    let startPage = Math.max(2, currentPage - 2); // Start at the page two before the current
    let endPage = Math.min(numPages - 1, currentPage + 3); // Show up to three pages after the current

    for (let i = startPage; i <= endPage; i++) {
      paginationHtml += `<li data-page="${i}" ${
        i === currentPage ? 'class="active"' : ""
      }>${i}</li>`;
    }

    if (endPage < numPages - 1) {
      paginationHtml += `<li>...</li>`;
    }

    paginationHtml += `<li data-page="${numPages}">${numPages}</li>`;

    paginationHtml += `<li data-page="${currentPage + 1}" ${
      currentPage === numPages ? 'class="disabled"' : ""
    }>
      <svg width="5" height="8" viewBox="0 0 5 8" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4.35365 4.35355C4.54892 4.15829 4.54892 3.84171 4.35365 3.64645L1.17167 0.464466C0.976411 0.269204 0.659828 0.269204 0.464566 0.464466C0.269304 0.659728 0.269304 0.976311 0.464566 1.17157L3.29299 4L0.464566 6.82843C0.269304 7.02369 0.269304 7.34027 0.464566 7.53553C0.659828 7.7308 0.976411 7.7308 1.17167 7.53553L4.35365 4.35355ZM4 4.5H4.0001V3.5H4V4.5Z" fill="#676767" />
      </svg>
    </li>`;

    paginationHtml += `<li data-page="${numPages}" ${
      currentPage === numPages ? 'class="disabled"' : ""
    }>
    <svg width="9" height="8" viewBox="0 0 9 8" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M4.35355 4.35355C4.54881 4.15829 4.54881 3.84171 4.35355 3.64645L1.17157 0.464466C0.976304 0.269204 0.659721 0.269204 0.464459 0.464466C0.269197 0.659728 0.269197 0.976311 0.464459 1.17157L3.29289 4L0.464459 6.82843C0.269197 7.02369 0.269197 7.34027 0.464459 7.53553C0.659721 7.7308 0.976304 7.7308 1.17157 7.53553L4.35355 4.35355ZM3.99989 4.5H3.99999V3.5H3.99989V4.5Z" fill="#676767" />
      <path d="M8.35355 4.35355C8.54881 4.15829 8.54881 3.84171 8.35355 3.64645L5.17157 0.464466C4.9763 0.269204 4.65972 0.269204 4.46446 0.464466C4.2692 0.659728 4.2692 0.976311 4.46446 1.17157L7.29289 4L4.46446 6.82843C4.2692 7.02369 4.2692 7.34027 4.46446 7.53553C4.65972 7.7308 4.9763 7.7308 5.17157 7.53553L8.35355 4.35355ZM7.99989 4.5H7.99999V3.5H7.99989V4.5Z" fill="#676767" />
    </svg>
    </li>`;

    $("#pagination_organization ul").html(paginationHtml);
  }

  $(document).on("click", "#pagination_organization ul li", function () {
    const page = $(this).data("page");
    if (page && !$(this).hasClass("disabled")) {
      loadOrganizations(page);
    }
  });

  loadOrganizations(1);
});
