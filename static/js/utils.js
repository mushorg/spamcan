$(function() {
	    $('button#get_stats').bind('click', function() {
	      $.ajax({
                    type: 'POST',
                    url: '/stats',
                    data: {id: $(this).attr("value")},
                    success: function(response) {
                        $('#count').html(response);
                    }
                });
	      return false;
	    });
	  });