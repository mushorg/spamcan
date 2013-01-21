$(function() {
	$('button#get_stats').bind('click', function() {
		$(this).button();
		$(this).button('loading');
		var acc_id = $(this).attr("value");
		$.ajax({
			type: 'POST',
			url: '/get_stats',
			data: {id: acc_id},
			success: function(response) {
				$('#count' + acc_id).html(response);
				$('button#get_stats').button('reset');
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
	$('button#fetch_mails').bind('click', function() {
       var ids = new Array();
       $("input[type='checkbox']:checked").each(function() {
            ids.push($(this).val());
       });
       $.ajax({
            type: 'POST',
            url: '/fetch_mails',
            data: {ids: JSON.stringify(ids)},
            success: function(response) {
                alert(JSON.parse(response));
            }
        });
        return false;
	});
});