$(function() {
	$('button#get_stats').bind('click', function() {
		var acc_id = $(this).attr("value");
		$.ajax({
			type: 'POST',
			url: '/get_stats',
			data: {id: acc_id},
			success: function(response) {
				$('#count' + acc_id).html(response);
			}
		});
		return false;
	});
	$('button#delete_acc').bind('click', function() {
		var acc_id = $(this).attr("value");
		var r=confirm("Are you sure you want to delete account #" + acc_id + "?");
		if (r==true){
			$.ajax({
			type: 'POST',
			url: '/delete_acc',
			data: {id: acc_id},
			success: function(response) {
				if(response == "True"){
					$('#notice').html("Account #" + acc_id + " deleted");
					$('tr#row' + acc_id).html('');
				} else {
					$('#notice').html(response);
				}
			}
			});
		} else {
			return false;
		}
	});
});