$(document).ready(function(){
	$.ajaxSetup({ cache: false});
	
	$("#searchBar" ).autocomplete({
		source: "/ratemycscourse/search/",

		select: function( event, ui ) { 
			window.location.pathname = "ratemycscourse/" + ui.item.value;
        }
	});
});
