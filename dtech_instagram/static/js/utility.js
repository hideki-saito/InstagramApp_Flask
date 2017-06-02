function croppie_activate() {
    var $img = $("#img");

    if ($(".croppie-container").length) {
        c.destroy();
        $img.unwrap();
    }

    $('#img').css('display', 'none');

    viewport_width = 200
    viewport_height = 200

    c = new Croppie(document.getElementById('img'), {
        viewport: {
            width: viewport_width,
            height: viewport_height
        }
    });

//    c.bind({url: document.getElementById('img').getAttribute('src'), points: [77,469,280,739]});

    $('.cr-slider-wrap').css({'margin': '15px 0px', 'display': 'flex', 'width': '100%', 'justify-content': 'space-around'});
    $('.cr-slider').css('width', '70%');
    $('.cr-slider-wrap').append("<button id='cropping'>CROPPING</button>");

    function popupResult(result) {
		var html;
		if (result.html) {
			html = result.html;
		}
		if (result.src) {
			html = '<img src="' + result.src + '" />';
		}
		swal({
			title: '',
			html: true,
			text: html,
			allowOutsideClick: true
		});
		setTimeout(function(){
			$('.sweet-alert').css('margin', function() {
				var top = -1 * ($(this).height() / 2),
					left = -1 * ($(this).width() / 2);

				return top + 'px 0 0 ' + left + 'px';
			});
		}, 1);
	}

    $("#cropping").click(function() {
        image_deletion()

        var zoom = c.get()['zoom']
        var zoom_reverse = 1 / zoom
        var cropping_width = parseInt(viewport_width * zoom_reverse, 10);
        var cropping_height = parseInt(viewport_height * zoom_reverse, 10);
        var cropping_size = { width: cropping_width, height: cropping_height };
        console.log(cropping_size)

        c.result({type:'canvas', format:'jpeg', size:cropping_size}).then(function(result) {
            $('#img').css('display', 'block');
            $("#img").attr('src', result);
            $("#url").val(result);
            c.destroy();
            $('#img').unwrap()
        })
    });
}

function place_image(url) {
    $("#img").attr('src', url);
    $("#url").val(url);

    croppie_activate();
}

function image_deletion() {
    uri = $('#img').attr('src')
    if (uri.indexOf(urlPrefix) >= 0) {
        uri_pieces = uri.split("/")
        uri_main = uri_pieces[uri_pieces.length-1]
        ajax_functions.delete_image(uri_main, 'upload')
    }
}


