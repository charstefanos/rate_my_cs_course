$(document).ready(function(){
        $("#id_current_student").click(function(){
			if($("#id_current_student").is(':checked')){
				$("div#current_student_fields").removeAttr("hidden");
			}else{
				$("div#current_student_fields").attr("hidden",true);
			}
					
		});
});