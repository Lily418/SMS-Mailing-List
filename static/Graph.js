WEB_SOCKET_DEBUG = true;


$( document ).ready(function() {
	
io.configure(function () { 
  io.set("transports", ["xhr-polling"]); 
  io.set("polling duration", 10); 
});

var socket = io.connect('/Vote');
socket.on('vote', voteRecived);
});

function voteRecived(vote)
{
	alert(JSON.stringify(vote));
}
