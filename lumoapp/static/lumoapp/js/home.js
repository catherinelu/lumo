	$(function() {
		$( ".event-entry-overview" ).click(function() {
		// $( ".event-entry-overview" ).click(function() {
			// 	console.log($( this ).css( "background-color"));
			$( this ).css( "background-color", "FCFEF5");
			var cur_detail =  $( this ).next('.event-entry-detail');
			if (cur_detail.is( ":hidden" ) ) {
		    cur_detail.slideDown();
		  } else {
		  	$( this ).css( "background-color", "FFFFFF");
		    cur_detail.slideUp();
		  }
		});

	  // cut the tail of text that's too long
	  $( ".event-description-div" ).each(function( index ) {
	  	var text = $( this ).text()
	  	if (text.length > 18) {
	  		$(this).html(text.substr(0, 18) + '...')
	  	}
		});

	  $( ".event-detail-location-div" ).each(function( index ) {
	  	var text = $( this ).text()
	  	if (text.length > 0) {
	  		$(this).html('@' + text)
	  	}
		});

		var $alert = $('.alert');
	  $alert.modal();

		$("#footer-alarm-div").click(function() {
			$alert.modal('show');
	  	$alert.css('display', 'block');
		  $alert.find('.modal-content').html("Alarm clock");
		});

		$alert.on('hide.bs.modal', function() {
      console.log("model goes away now!")
    });

		$("#footer-bed-div").click(function() {
			$alert.modal('show');
	  	$alert.css('display', 'block');
		  $alert.find('.modal-content').html("Bed time");
		});
	});
