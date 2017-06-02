$(document).ready(function () {
    $('#exampleModal').modal('show');
    showDashboardEmbedModal();

    $('#addEmailAddress').on('click', function (event) {
        var emailAddress = $("#user-email-address").val();
        event.preventDefault();
        isEmail(emailAddress);
    })

    $('.switch-accounts').on('click touchstart', function (event) {
        event.preventDefault();
        logOutOfInstagramAndSocialmeans();
        return false;
    });

    $('[data-toggle="tooltip"]').tooltip()
});

// Add the number shortening
var pow = Math.pow, floor = Math.floor, abs = Math.abs, log = Math.log;

function round(n, precision) {
    var prec = Math.pow(10, precision);
    return Math.round(n * prec) / prec;
}

// validate email address
function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (regex.test(email)) {
        updateAccountEmailAddress(email)
    } else {
        //TODO add validation logic to the form
        $("#exampleModalLabel").html('Please provide a valid email address!');
    }
}

function updateAccountEmailAddress(email) {
    $.ajax({
        type: 'POST',
        data: {email: email, csrfmiddlewaretoken: csrftoken},
        dataType: 'json',
        url: '/api/account/update-email-address/',
        success: function (data) {
            $(".form-group").hide();
            $("#addEmailAddress").hide();
            $("#exampleModalLabel").html('Thank you!');
            $(".close-modal").show();
        },
        error: function (request, status, error) {
            // todo: add error over chart with option to refresh?
            $("#exampleModalLabel").html('Whoops, something went wrong. Please refresh and try again.');
        }
    });
}

function logOutOfInstagramAndSocialmeans() {
    $("#logoutIgIframe").html('<iframe src="https://www.instagram.com/accounts/logout/"/>');
    $.get("/logout");
    $("#overlay").show();
    setTimeout(function () {
        window.location = "/login/instagram";
    }, 2500);
}

// Get the cookie to pass in POST request
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');