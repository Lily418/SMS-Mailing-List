WEB_SOCKET_DEBUG = true;


$( document ).ready(function() {
var socket = io.connect('/Vote');
socket.on('vote', voteRecived);
});

function voteRecived(vote)
{
	alert(JSON.stringify(vote));
}
