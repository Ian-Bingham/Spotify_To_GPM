$(document).ready(function () {
    // make the tables selectable
    $(".spotify_table").multiSelect({actcls: 'ui-selected'});
    $(".gpm_table").multiSelect({actcls: 'ui-selected'});

    // close the popup when they click the X
    $('.close_popup').on('click', function () {
        $(this).parent().parent().parent()[0].style.display = 'none'
    })

    // display the loading popup when importing songs
    $(".import_links a").on('click', function() {
        $(".popup_wrapper").show()
        $(".loader_popup").show();
        $(".songs_popup").hide();
    })

    $(".spotify_to_gpm").on('click', function () {
        // display the loading popup when transferring songs
        let spotify_track_list = [];
        $(".popup_wrapper").show()
        $(".loader_popup").show();
        $(".songs_popup").hide();

        // get all of the selected Spotify songs and save them in a list
        $(".spotify_song").each(function () {
            if ($(this).hasClass('ui-selected')) {
                let track = {};
                track['name'] = $(this).children('td.spotify_name').text();
                track['artist'] = $(this).children('td.spotify_artist').text();
                track['album'] = $(this).children('td.spotify_album').text();
                spotify_track_list.push(track)
            }
        });

        // send the list of selected Spotify songs to Django
        $.ajax({
            type: 'POST',
            url: '/capstone/spotify_to_gpm/',
            data: {'spotify_track_list': JSON.stringify(spotify_track_list)},
            success: function (data) {
                // data: the JSON object that our Django view 'spotify_to_gpm' returns
                let spotify_tracks_added = data['spotify_tracks_added']
                let spotify_tracks_not_added = data['spotify_tracks_not_added']


                // update our h3 header
                $(".added_songs h3").text(`The following ${spotify_tracks_added.length} songs were added to your GPM Library:`)
                $(".not_added_songs h3").text(`The following ${spotify_tracks_not_added.length} songs were NOT added to your GPM Library:`)
                update_popup(spotify_tracks_added, spotify_tracks_not_added)
            },
            error: function (data) {
                console.log('ajax error')
                console.log(data)
            },
        })
    });

    $(".gpm_to_spotify").on('click', function () {
        // display the loading popup when transferring songs
        let gpm_track_list = [];
        $(".popup_wrapper").show()
        $(".loader_popup").show();
        $(".songs_popup").hide();

        // get all of the selected GPM songs and save them in a list
        $(".gpm_song").each(function () {
            if ($(this).hasClass('ui-selected')) {
                let track = {};
                track['name'] = $(this).children('td.gpm_name').text();
                track['artist'] = $(this).children('td.gpm_artist').text();
                track['album'] = $(this).children('td.gpm_album').text();
                gpm_track_list.push(track)
            }
        });

        // send the list of selected GPM songs to Django
        $.ajax({
            type: 'POST',
            url: '/capstone/gpm_to_spotify/',
            data: {'gpm_track_list': JSON.stringify(gpm_track_list)},
            success: function (data) {
                // data: the JSON object that our Django view 'gpm_to_spotify' returns
                let gpm_tracks_added = data['gpm_tracks_added'];
                let gpm_tracks_not_added = data['gpm_tracks_not_added'];

                // update our h3 header
                $(".added_songs h3").text(`The following ${gpm_tracks_added.length} songs were added to your Spotify Library:`)
                $(".not_added_songs h3").text(`The following ${gpm_tracks_not_added.length} songs were NOT added to your Spotify Library:`)
                update_popup(gpm_tracks_added, gpm_tracks_not_added);
            },
            error: function (data) {
                console.log('ajax error')
                console.log(data)
            },
        })
    });
});

function update_popup(tracks_added, tracks_not_added) {
    // empty the table from previous transfers
    $(".popup_table_added tbody").empty()
    $(".popup_table_not_added tbody").empty()

    // add rows of data to the songs added table
    for (let i = 0; i < tracks_added.length; i++) {
        let name = tracks_added[i]['name']
        let artist = tracks_added[i]['artist']
        let album = tracks_added[i]['album']
        $(".popup_table_added tbody").append(`<tr> <td>${name}</td> <td>${artist}</td> <td>${album}</td> </tr>`)
    }

    // add rows of data to the songs not added table
    for (let i = 0; i < tracks_not_added.length; i++) {
        let name = tracks_not_added[i]['name']
        let artist = tracks_not_added[i]['artist']
        let album = tracks_not_added[i]['album']
        $(".popup_table_not_added tbody").append(`<tr> <td>${name}</td> <td>${artist}</td> <td>${album}</td> </tr>`)
    }

    // hide the loader and show our add/not_added song tables
    $(".loader_popup").hide();
    $(".songs_popup").show();
}
