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
      npUpdate(data.videoId, data.title)
      break
    case "oneQueued":
      break
    case "refresh":
      refresh()
      break
    case "newUser":
      document.cookie = "crushistUserId=" + data.newUserId +
      "; expires=Fri, 31 Dec 2100 12:00:00 UTC; path=/"
      vote(0, 0)
      break
    case "connected":
      if (!idParse()) {
        socket.send(JSON.stringify({"action": "newUser"}))
      } else {
        vote(0, 0)
      }
      npUpdate(data.videoId, data.title)
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
      maxResults: 5,
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
  var song = `<div class="songadder" id="${entry.id.videoId}"
    onclick="queueSong('${entry.id.videoId}')">${entry.snippet.title}</div>`
  return song;
}

function queueSong(code) {
  console.log($("#" + code).html())
  socket.send(JSON.stringify({
    "action": "queueSong",
    "title": $("#" + code).html(),
    "yt_url": code
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

function npUpdate(code, title) {
  var img = 'https://i.ytimg.com/vi/' + code + '/hqdefault.jpg'
  $('#npImg').css("background-image", "url(" + img + ")")
  $('#npTitle').html(title)
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