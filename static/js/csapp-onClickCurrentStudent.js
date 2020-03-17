$(document).ready(function(){
	$.ajaxSetup({ cache: false });
	$("#id_current_student").click(function(){
		if($("#id_current_student").is(':checked')){
			$("div#current_student_fields").removeAttr("hidden");
		}else{
			$("div#current_student_fields").attr("hidden",true);
			$("#id_year_of_studies").val(null);
			$("#id_courses").val(null);
			$("#id_contact").prop( "checked", false );
			
		}
					
	});
});