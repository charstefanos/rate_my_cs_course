$(document).ready(function(){
	$.ajaxSetup({ cache: false});
	
	$("#searchBar" ).autocomplete({
		source: function(request, response) {
		$.ajax({
			url: "/ratemycscourse/search/",
			type: "GET",
			dataType: "json",
			data: {
				term: $("#searchBar").val()
			},
			success: function(data) {
				var array = $.map(data, function(item) {
					return {
						label: item.label,
						value: item.value
					};
				});
                response($.ui.autocomplete.filter(array, request.term));
        }
    });
},
		select: function( event, ui ) { 
			window.location.pathname = "ratemycscourse/" + ui.item.value;
        }
	});
});
