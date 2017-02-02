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
        origin: 'http://crushist.herokuapp.com',
        autoplay: '0',
        iv_load_policy: '3'
      },
      events: {
        'onStateChange': onPlayerStateChange
      }
    })
}


// ************************* Cookie Handler *************************
if (!) {
  if (socket.readyState == WebSocket.OPEN) {
    socket.send(JSON.stringify({"action": "newUser"}))
  }
}


// ************************* Socket Constructor *************************
var ws_p = window.location.protocol == "https:" ? "wss" : "ws"
var pagename = window.location.host + window.location.pathname
socket = new WebSocket(ws_p + "://" + pagename)

socket.onmessage = function(e) {
  var data = JSON.parse(e.data)

  switch(data.action) {
    case "newVote":
      $("#song" + data.songId + "votes").html(data.votes)
      break
    case "voted":
      $("#song" + data.songId + data.vote).css("color", "red")
      break
    case "nextSong":
      player.loadVideoById(data.videoId)
      break
    case "refresh":
      refresh()
      break
    case "newUser":
      localStorage.setItem(27875, "{'userId':'" + data.newUserId +"'}")
      break
    default:
      alert("something went wrong with your switch")
  }
}


// ************************* YouTube Control *************************
function onPlayerStateChange(event) {
  if (event.data == 0 && socket.readyState == WebSocket.OPEN) {
    socket.send(JSON.stringify({"action": "nextSong"}))
  }
}

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
        $("#search-results").append(songHtml(data.items[i]))
      }
    });
}

function songHtml(entry) {
  var song = `<div class="songadder"
    onclick="queueSong('${entry.id.videoId}', '${entry.snippet.title}')">
    ${entry.snippet.title}<hr></div>`
  return song;
}

function queueSong(newSong, title) {
  if (socket.readyState == WebSocket.OPEN) {
    socket.send(JSON.stringify({
      "action": "queueSong",
      "title": title,
      "yt_url": newSong,
    }))
  }

  $("#query").val("")
  $("#search-results").empty()
}


// ***************************** Playlist Loader *****************************
refresh()
function refresh() {
  $.get(
      window.location.href + "playlist",
      function(data) {
        $(".playlist").html(data)
      }
  )
}


// ******************************* Voting *******************************
function vote(songId, vote) {
  if (socket.readyState == WebSocket.OPEN) {
    socket.send(JSON.stringify({
        "action": "vote",
        "userId": localStorage.getItem(27875),
        "songId": songId,
        "vote": vote,
    }))
  }
}
