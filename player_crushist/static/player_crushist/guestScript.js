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
