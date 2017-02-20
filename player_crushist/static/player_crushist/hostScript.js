// ************************* YouTube Player *************************
var tag = document.createElement('script')
tag.src = "https://www.youtube.com/player_api"
var firstScriptTag = document.getElementsByTagName('script')[0]
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)

var player;
function onYouTubePlayerAPIReady() {
    player = new YT.Player('ytplayer', {
      height: $('#content').width() * 9 / 16,
      width: '100%',
      videoId: '',
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
  if (event.data == -1 && !player.getVideoData().video_id) {
    socket.send(JSON.stringify({"action": "nextSong"}))
  }
}


// ************************* Message Handling *************************
socket.onmessage = function(e) {
  var data = JSON.parse(e.data)

  switch(data.action) {
    case "voted":
      upvoted = data.upvoted
      downvoted = data.downvoted
      break
    case "nextSong":
      player.loadVideoById(data.videoId)
      break
    case "oneQueued":
      if (player.getPlayerState() < 1) {
        socket.send(JSON.stringify({"action": "nextSong"}))        
      }
      break
    case "refresh":
      refresh()
      break
    case "newUser":
      document.cookie = "crushistUUID=" + data.newUserId +
      "; expires=Fri, 31 Dec 2100 12:00:00 UTC; path=/"
      vote(0, 0)
      break
    case "connected":
      if (!idParse()) {
        socket.send(JSON.stringify({"action": "newUser"}))
      } else {
        vote(0, 0)
      }
      break
    default:
      console.log("something went wrong with your switch")
  }
}
