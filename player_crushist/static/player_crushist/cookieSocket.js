// ************************* Socket Constructor *************************
var ws_p = window.location.protocol == "https:" ? "wss" : "ws"
var pagename = window.location.host + window.location.pathname
socket = new WebSocket(ws_p + "://" + pagename)

// ************************** Cookie Handlers **************************
function idParse() {
  var b = document.cookie.match('(^|;)\\s*' + "crushistUserId" + '\\s*=\\s*([^;]+)');
  return b ? b.pop() : '';
}