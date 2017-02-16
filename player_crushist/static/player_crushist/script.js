// ************************* Socket Constructor *************************
var ws_p = window.location.protocol == "https:" ? "wss" : "ws"
var pagename = window.location.host + window.location.pathname
socket = new WebSocket(ws_p + "://" + pagename)

var upvoted = []
var downvoted = []

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
      console.log("thing")
      if (player.getPlayerState() < 1) {
        player.loadVideoById(data.videoId)
      }
      break
    case "refresh":
      refresh()
      break
    case "newUser":
      document.cookie = "crushistUserId=" + data.newUserId + ";path=/"
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


// ************************* YouTube Control *************************
function searchListByKeyword() {
  var q = $("#query").val()
  if (q == "") {
    $("#search-results").empty()
    return
  }
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
      $("#search-results").empty()
      for(var i in data.items) {
        $("#search-results").append(songHtml(data.items[i]))
      }
    });
}

function songHtml(entry) {
  var song = `<div class="songadder"
    onclick='queueSong("${entry.id.videoId}", "${entry.snippet.title}")'>
    ${entry.snippet.title}</div>`
  return song;
}

function queueSong(newSong, title) {
  socket.send(JSON.stringify({
    "action": "queueSong",
    "title": title,
    "yt_url": newSong
  }))

  $("#query").val("")
  $("#search-results").empty()
}


// ***************************** Playlist Loader *****************************
function refresh() {
  $.get(
      window.location.href + "playlist",
      function(data) {
        $(".playlist").html(data)
        for (var i = 0; i < upvoted.length; i++) {
          $("#song" + upvoted[i] + "up").css("color", "blue")
        }
        for (var i = 0; i < downvoted.length; i++) {
          $("#song" + downvoted[i] + "down").css("color", "red")
        }
      }
  )
}


// ******************************* Voting *******************************
function vote(songId, vote) {
  socket.send(JSON.stringify({
      "action": "vote",
      "userId": idParse(),
      "songId": songId,
      "vote": vote,
  }))
}


// ************************** Button Redirect **************************
function newEvent() {
  location.pathname = "/create"
}

function join() {
  location.pathname = "/" + $("#joincode").val()
}

// ************************** Cookie Handlers **************************
function idParse() {
  var b = document.cookie.match('(^|;)\\s*' + "crushistUserId" + '\\s*=\\s*([^;]+)');
  return b ? b.pop() : '';
}