$(document).ready(function(){
	$.ajaxSetup({ cache: false });
	$("#view_all_reviews_button").click(function(){
		$(".hidden_reviews").removeAttr("hidden");
		$("#view_all_reviews_button").attr("hidden",true);			
	});
});