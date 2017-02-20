var upvoted = []
var downvoted = []

// ***************************** Playlist Loader *****************************
function refresh() {
  $.get(
      window.location.href + "playlist",
      function(data) {
        $(".playlist").html(data)
        for (var i = 0; i < upvoted.length; i++) {
          $("#song" + upvoted[i] + "votes").css("color", "red")
        }
        for (var i = 0; i < downvoted.length; i++) {
          $("#song" + downvoted[i] + "votes").css("color", "blue")
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
  var song = `<div class="songadder" onclick="queueSong('${entry.id.videoId}')">
      <div id="${entry.id.videoId}Title" style="font-weight: bold;">${entry.snippet.title}</div>
      <div id="${entry.id.videoId}Channel">${entry.snippet.channelTitle}</div>
    </div>`
  // var song = `<div class="songadder" id="${entry.id.videoId}"
    // onclick="queueSong('${entry.id.videoId}')">${entry.snippet.title}</div>`
  return song;
}

function queueSong(code) {
  socket.send(JSON.stringify({
    "action": "queueSong",
    "title": $("#" + code + "Title").html(),
    "yt_url": code,
    "channel": $("#" + code + "Channel").html()
  }))

  $("#query").val("")
  $("#search-results").empty()
}