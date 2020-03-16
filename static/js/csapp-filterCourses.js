 $(document).ready(function(){
	 $("#id_year_of_studies").change(function () {
		var url = $("#user_form").attr("data_courses_url");  
		var yearOfStudies = $(this).val();  
	 
		$.ajax({
			url: url,
			data: {
				'year_of_studies': yearOfStudies
			},
			success: function (data) {
				$("#id_courses").html(data);
			}
		});
	});
 });
