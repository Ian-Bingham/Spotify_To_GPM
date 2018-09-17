$(document).ready(function() {
    $("#spotify_selectable tbody").selectable();
    $("#gpm_selectable tbody").selectable();



    // $('.spotify_song').click(function () {
    //     $(this).toggleClass('ui-selected');
    // });
    // $('.gpm_song').click(function () {
    //     $(this).toggleClass('ui-selected');
    // });
    // $('.spotify_song').click(function (evt) {
    //     if (evt.shiftKey){
    //         //store las t el selected and if second click is the same remove it from var else select all between then remove selected
    //         console.log(this);
    //         $(this).toggleClass('ui-selected');
    //
    //     } else {
    //         $(this).toggleClass('ui-selected');
    //     }
    // })
});


$(".spotify_to_gpm").on('click', function() {
    // let spotify_song_ids = [];
    let spotify_track_list = [];
    $(".spotify_song").each(function(){
        if($(this).hasClass('ui-selected')) {
            // spotify_song_ids.push($(this).attr('id'))
            let track = {};
            track['name'] = $(this).children('td.spotify_name').text();
            track['artist'] = $(this).children('td.spotify_artist').text();
            track['album'] = $(this).children('td.spotify_album').text();
            spotify_track_list.push(track)
        }
    });
    // alert(spotify_song_ids)
    // alert(spotify_track_list);

    $.ajax({
        type: 'POST',
        url: '/capstone/spotify_to_gpm/',
        // data: {'spotify_song_ids': JSON.stringify(spotify_song_ids)},
        data: {'spotify_track_list': JSON.stringify(spotify_track_list)},
        success: function (data) {
             //this gets called when server returns an OK response
             // alert("it worked!");
        },
        error: function (data) {
             // alert("it didnt work");
        },
    })
});

$(".gpm_to_spotify").on('click', function() {
    let gpm_song_ids = [];
    $(".gpm_song").each(function(){
        if($(this).hasClass('ui-selected')) {
            gpm_song_ids.push($(this).attr('id'))
        }
    })
    alert(gpm_song_ids)
});