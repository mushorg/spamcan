$(function() {
	$('button#get_stats').bind('click', function() {
		$.ajax({
			type: 'POST',
			url: '/get_stats',
			data: {id: $(this).attr("value")},
			success: function(response) {
				$('#count').html(response);
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
				$('#notice').html(response);
				$('tr#row' + acc_id).html('');
			}
			});
		} else {
			return false;
		}
	});
});