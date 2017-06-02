/**
 * Created by Boss on 1/1/17.
 */
var loadingHtml = '<div class="row"> <div class="sk-fading-circle"><div class="sk-circle1 sk-circle"></div><div class="sk-circle2 sk-circle"></div> <div class="sk-circle3 sk-circle"></div> <div class="sk-circle4 sk-circle"></div> <div class="sk-circle5 sk-circle"></div> <div class="sk-circle6 sk-circle"></div> <div class="sk-circle7 sk-circle"></div> <div class="sk-circle8 sk-circle"></div> <div class="sk-circle9 sk-circle"></div> <div class="sk-circle10 sk-circle"></div> <div class="sk-circle11 sk-circle"></div> <div class="sk-circle12 sk-circle"></div> </div> </div>'

function makeAjaxCallForEmbed(link, modal) {
    try {
        $.ajax({
        type: 'GET',
        url: '/api/embed-html/?url=' + link + '&OMITSCRIPT=true',
        success: function (data) {
            modal.html(data);
            instgrm.Embeds.process();
            $('#myModal').modal('show');
        }
        })
    } catch (e) {
        modal.html(e);
        console.log(e);
    }
}

function showDashboardEmbedModal(){
    $('.dashboard-modal').on('click', function() {
        var modal = $('.modal-body');
        modal.html(loadingHtml);
        var instaLink = $(this).data('link');
        makeAjaxCallForEmbed(instaLink, modal);
    });
}

function showContentEmbedModal(){
    $('#myModal').on('shown.bs.modal', function (e) {
        var modal = $('.modal-body');
        modal.html(loadingHtml);
        var instaLink = $(e.relatedTarget).data('link');
        makeAjaxCallForEmbed(instaLink, modal);
    });
}