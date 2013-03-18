Reveal.initialize({
	controls: true,
	progress: true,
	history: true,
	center: true,

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

Reveal.addEventListener('slidechanged', function(event){
	var c = new Array();
	h = event.indexh;
	v = event.indexv;
	$.post("/event/currentslide", {'indexh': h, 'indexv': v}, function(data){console.log(data)});
});

presence = function() {
	$.get('/event/presence', function(p){
		Messenger().post("Online watchers: "+ p);
	});
};

setInterval(presence, 30000); // 1 min
