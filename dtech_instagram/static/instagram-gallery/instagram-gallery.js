$.fn.myig = function(username, password, id) {
    var k = ($(this).attr("id") != null || $(this).attr("id") != undefined ? '#' + $(this).attr("id") : '.' + $(this).attr("class"));
    $(this).html('<div class="myig_profile"></div><div class="myig_gallery"></div>');
    myig_profile(k);
    //myig_gallery(k, "");

    function myig_profile(c) {
        $.getJSON($SCRIPT_ROOT+'/ins_profile', {
            username: username,
            password: password,
            id: id
            }, function(data) {
            var b = '';
            b += '<div class="user_pic">';
            b += '	<img src="' + data.profile_pic_url + '" alt="" title="' + data.ins_username + ' on instagram">';
            b += '</div>';
            b += '<p class="user_name"><a href="http://instagram.com/' + data.ins_username + '" target="_BLANK">' + data.ins_username + '</a></p>';
            b += '<p>Name: ' + data.ins_fullname + '</p>';
            b += '<p>Bio: ' + data.biography + '</p>';
            b += '<p>Website: <a href="' + data.website + '" target="_BLANK">' + data.website + '</a></p>';
            //b += '<p><strong>' + data.posts.length + '</strong> posts | <strong>' + data.follower_count + '</strong> followers | <strong>' + data.following_cout + '</strong> following</p>';
            $(c + ' .myig_profile').html(b)
        })
    }

    function myig_gallery(e, f) {
        $.ajax({
            url: 'https://api.instagram.com/v1/users/' + g + '/media/recent/?access_token=' + j + '&count=' + h + '&max_id=' + f,
            crossDomain: true,
            dataType: 'jsonp'
        }).done(function(c) {
            var d = '';
            $.each(c.data, function(i, a) {
                var b = '';
                b += (c.data[i].caption == null || c.data[i].caption == undefined ? Date(c.data[i].created_time) : c.data[i].caption.text + ' - ' + Date(c.data[i].created_time));
                d += '<div class="user_gallery">';
                d += '	<a href="' + c.data[i].images.standard_resolution.url.replace(/\\/, "") + '" class="myig_popup" rel="myig_popup" title="' + b + '">';
                d += '		<img src="' + c.data[i].images.thumbnail.url.replace(/\\/, "") + '" alt="" title="' + b + '">';
                d += '	</a>';
                d += '</div>'
            });
            if (c.pagination.next_max_id != null && c.pagination.next_max_id != undefined) {
                d += '<div class="load_more"><span class="btn myig_more" data-next="' + c.pagination.next_max_id + '">MORE</span></div>'
            }
            $(e + ' .myig_gallery').append(d);
            $('.myig_more').click(function() {
                myig_gallery(e, $(this).data('next'));
                $(e + ' .load_more').remove();
                return false
            })
        })
    }
}
