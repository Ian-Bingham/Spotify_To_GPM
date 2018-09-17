$(document).ready(function() {
//     $("#spotify_table tbody").selectable();
//     $("#gpm_table tbody").selectable();

    $(".spotify_table").multiSelect({actcls: 'ui-selected'});


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
    let spotify_track_list = [];
    $(".spotify_song").each(function(){
        if($(this).hasClass('ui-selected')) {
            let track = {};
            track['name'] = $(this).children('td.spotify_name').text();
            track['artist'] = $(this).children('td.spotify_artist').text();
            track['album'] = $(this).children('td.spotify_album').text();
            spotify_track_list.push(track)
        }
    });

    $.ajax({
        type: 'POST',
        url: '/capstone/spotify_to_gpm/',
        data: {'spotify_track_list': JSON.stringify(spotify_track_list)},
        success: function (data) {
            let spotify_tracks_added = data['spotify_tracks_added']
            let spotify_tracks_not_added = data['spotify_tracks_not_added']

            $(".added_to_gpm ul").empty()
            $(".not_added_to_gpm ul").empty()

            for (let i=0; i < spotify_tracks_added.length; i++){
                let name = spotify_tracks_added[i]['name']
                let artist = spotify_tracks_added[i]['artist']
                let album = spotify_tracks_added[i]['album']
                $(".added_to_gpm ul").append(`<li>Title: ${name}, Artist: ${artist}, Album: ${album}</li>`)
            }

            for (let i=0; i < spotify_tracks_not_added.length; i++){
                let name = spotify_tracks_not_added[i]['name']
                let artist = spotify_tracks_not_added[i]['artist']
                let album = spotify_tracks_not_added[i]['album']
                $(".not_added_to_gpm ul").append(`<li>Title: ${name}, Artist: ${artist}, Album: ${album}</li>`)
            }

            $(".gpm_popup_wrapper").show()
        },
        error: function (data) {
            console.log('ajax error')
            console.log(data)
        },
    })
});

$(".gpm_to_spotify").on('click', function() {
    let gpm_track_list = [];
    $(".gpm_song").each(function(){
        if($(this).hasClass('ui-selected')) {
            // spotify_song_ids.push($(this).attr('id'))
            let track = {};
            track['name'] = $(this).children('td.gpm_name').text();
            track['artist'] = $(this).children('td.gpm_artist').text();
            track['album'] = $(this).children('td.gpm_album').text();
            gpm_track_list.push(track)
        }
    });

    $.ajax({
        type: 'POST',
        url: '/capstone/gpm_to_spotify/',
        data: {'gpm_track_list': JSON.stringify(gpm_track_list)},
        success: function (data) {
            let gpm_tracks_added = data['gpm_tracks_added']
            let gpm_tracks_not_added = data['gpm_tracks_not_added']

            $(".added_to_spotify ul").empty()
            $(".not_added_to_spotify ul").empty()


            for (let i=0; i < gpm_tracks_added.length; i++){
                let name = gpm_tracks_added[i]['name']
                let artist = gpm_tracks_added[i]['artist']
                let album = gpm_tracks_added[i]['album']
                $(".added_to_spotify ul").append(`<li>Title: ${name}, Artist: ${artist}, Album: ${album}</li>`)
            }

            for (let i=0; i < gpm_tracks_not_added.length; i++){
                let name = gpm_tracks_not_added[i]['name']
                let artist = gpm_tracks_not_added[i]['artist']
                let album = gpm_tracks_not_added[i]['album']
                $(".not_added_to_spotify ul").append(`<li>Title: ${name}, Artist: ${artist}, Album: ${album}</li>`)
            }

            $(".spotify_popup_wrapper").show()
        },
        error: function (data) {
        },
    })
});