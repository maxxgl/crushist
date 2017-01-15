// ************************* YouTube Player *************************
var tag = document.createElement('script')
tag.src = "https://www.youtube.com/player_api"
var firstScriptTag = document.getElementsByTagName('script')[0]
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)

var player;
function onYouTubePlayerAPIReady() {
    player = new YT.Player('ytplayer', {
      height: '270',
      width: '480',
      videoId: '7LnBvuzjpr4',
      playerVars: {
        // origin: '', !!!! <--- Update for deployment
        autoplay: '0',
        iv_load_policy: '3'
      },
      events: {
        'onStateChange': onPlayerStateChange
      }
    })
}

function onPlayerStateChange(event) {
    if (event.data == 0) {
        event.target.loadVideoById('lasWefVUCsI');
    }
}


// ************************* YouTube Search *************************
function searchListByKeyword() {
    var q = $("#query").val();
    $.get( "https://www.googleapis.com/youtube/v3/search",
        {
            key: 'AIzaSyDHZf5lGSWfwmhjcsmVCFgNH41v76uG0ac',
            maxResults: 3,
            type: 'video',
            videoEmbeddable: 'true',
            part: 'snippet',
            q: q
        },
        function(data) {
            for(var i in data.items) {
                var item = data.items[i];
                $("#search-results").append("<img src='" + item.snippet.thumbnails.default.url + "'> </img>" + item.snippet.title + "<hr>")
            }
        });
}
