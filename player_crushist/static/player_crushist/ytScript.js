// ************************* YouTube Player *************************
var tag = document.createElement('script')
tag.src = "https://www.youtube.com/player_api"
var firstScriptTag = document.getElementsByTagName('script')[0]
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)

var player;
function onYouTubePlayerAPIReady() {
    var h = $('#ytplayer').width() * 9 / 16
    player = new YT.Player('ytplayer', {
      height: h,
      width: '100%',
      videoId: '7LnBvuzjpr4',
      playerVars: {
        origin: 'http://crushist.herokuapp.com',
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
    socket.send(JSON.stringify({"action": "nextSong"}))
  }
}
