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
	   $(this).button();
       $(this).button('loading');
       var ids = new Array();
       $("input[type='checkbox']:checked").each(function() {
            ids.push($(this).val());
       });
       $.ajax({
            type: 'POST',
            url: '/fetch_mails',
            data: {ids: JSON.stringify(ids)},
            success: function(response) {
                var res = JSON.parse(response);
                for (var key in res) {
                    $('#local_count' + key).html(res[key]);
                }
                $('button#fetch_mails').button('reset');
            }
        });
        return false;
	});
	$('button#crawl_mails').bind('click', function() {
       $(this).button();
       $(this).button('loading');
       var ids = new Array();
       $("input[type='checkbox']:checked").each(function() {
            ids.push($(this).val());
       });
       $.ajax({
            type: 'POST',
            url: '/crawl_mails',
            data: {ids: JSON.stringify(ids)},
            success: function(response) {
                var res = JSON.parse(response);
                for (var key in res) {
                    $('#urls' + key).html(res[key].length);
                }
                $('button#crawl_mails').button('reset');
            }
        });
        return false;
    });
	$("button#select_all").bind('click', function(){
	    var checkboxes = $("input[type='checkbox']");
        checkboxes.prop("checked", !checkboxes.prop("checked"));
    });
});

