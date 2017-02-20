// ************************* Socket Constructor *************************
var ws_p = window.location.protocol == "https:" ? "wss" : "ws"
var pagename = window.location.host + window.location.pathname
socket = new WebSocket(ws_p + "://" + pagename)

// ************************** Cookie Handlers **************************
function idParse() {
  var b = document.cookie.match('(^|;)\\s*' + "crushistUUID" + '\\s*=\\s*([^;]+)');
  return b ? b.pop() : '';
}


// ***************************** Google Analytics *****************************
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-92216536-1', 'auto');
ga('send', 'pageview');
