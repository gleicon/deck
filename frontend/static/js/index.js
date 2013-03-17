Reveal.initialize({
	controls: false,
	keyboard: false,
	progress: true,

	theme: Reveal.getQueryHash().theme,
	transition: Reveal.getQueryHash().transition || 'default',

	dependencies: [
		{ src: 'lib/js/classList.js', condition: function() { return !document.body.classList; } },
		{ src: 'plugin/markdown/showdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
		{ src: 'plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
		{ src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
		{ src: 'plugin/zoom-js/zoom.js', async: true, condition: function() { return !!document.body.classList; } },
		{ src: 'plugin/notes/notes.js', async: true, condition: function() { return !!document.body.classList; } },
        ]
});
            

update = function() {
	$.get("/event/currentslide", function(data){
	    e = JSON.parse(data)
	    Reveal.navigateTo(e.indexh, e.indexv);
	});
}

update();
Messenger().post("Connecting");		

if (!!window.EventSource) {
	var source = new EventSource('/event/live');
	source.addEventListener('message', function(e) {
	    data = JSON.parse(e.data);
	    console.log(data);
	    Reveal.navigateTo(data.indexh, data.indexv);
	}, false);
	
	source.addEventListener('open', function(e) {
		Messenger().post("Connected");		
	});

	source.addEventListener('close', function(e) {
		Messenger().post("You got disconnected");		
	});

	source.addEventListener('error', function(e) {
		Messenger().post({
 		  message: 'There was an error receiving events, try to reload',
  		  type: 'error',
  		  showCloseButton: true
		});

		console.log("error: "+ JSON.stringify(e)); 
	});

} else {
	setInterval(update, 60000); // 1 min                  
}

