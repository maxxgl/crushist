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


// ************************* Socket Constructor *************************
socket = new WebSocket("ws://" + window.location.host + "/event/1");

socket.onmessage = function(e) {
  var data = JSON.parse(e.data)

  switch(data.action) {
    case "newVote":
      $("#song" + data.songId + "votes").html(data.votes)
      break;
    case "voted":
      $("#song" + data.songId + data.vote).css("color", "red")
      break;
    case "nextSong":
      event.target.loadVideoById(data.videoId)
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
  console.log(entry)
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


// ******************************* Voting *******************************
function vote(id, vote) {
  if (socket.readyState == WebSocket.OPEN) {
    socket.send(JSON.stringify({
        "action": "vote",
        "songId": id,
        "vote": vote,
    }))
  }
}
