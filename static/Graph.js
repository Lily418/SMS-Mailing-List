var pusher = new Pusher('81830a54c2d8b0878390');
var channel = pusher.subscribe('vote_channel');
var r;

var a = new Array();


$( document ).ready(function() {

channel.bind('vote_event', function(vote) {
	vote = vote.message;
	if(vote in a)
	{
		a[vote]++;
	}
	else
	{
		a[vote] = 1;
	}
	
	//a.sort();
	//a.reverse();
	
	var voteArray = new Array();
	var labelArray = new Array();
	
	for (var key in a)
	{
		if (key === 'length' || !a.hasOwnProperty(key)) continue;
		var value = a[key];
		voteArray.push(value);
		labelArray.push(key);
		
	}
	
	drawPiChart(voteArray, labelArray);
	//drawPiChart([0,1,2], []);
	
});

r = Raphael(10, 100, 1400, 1400);
});

function drawPiChart(values, labels)
{
r.clear();
// Creates pie chart at with center at 320, 200,
// radius 100 and data: [55, 20, 13, 32, 5, 1, 2]
pie = r.piechart(400, 320, 300, values , { legend: labels, legendpos: "east"});
pie.hover(function () {
                    this.sector.stop();
                    this.sector.scale(1.1, 1.1, this.cx, this.cy);

                    if (this.label) {
                        this.label[0].stop();
                        this.label[0].attr({ r: 7.5 });
                        this.label[1].attr({ "font-weight": 800 });
                    }
                }, function () {
                    this.sector.animate({ transform: 's1 1 ' + this.cx + ' ' + this.cy }, 500, "bounce");

                    if (this.label) {
                        this.label[0].animate({ r: 5 }, 500, "bounce");
                        this.label[1].attr({ "font-weight": 400 });
                    }
                });

}