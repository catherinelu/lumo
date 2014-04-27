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

		$("#footer-alarm-div").click(function() {
			var $alert = $('.alarm-modal');
			$alert.modal('show');
	  	$alert.css('display', 'block');

	  	// fill in the set timing 
	  	var $set_row = $( ".alarm-set-div" );

	  	// added the input boxes
	  	$set_row.html("Wake me up at &nbsp; <span class='alarm-time-span'> \
	  		<input class='time-input-div' type='number' min='0' max='23' name='input-hour' id='input-hour' value='08'> : \
	  		<input  class='time-input-div' type='number' min='0' max='59' name='input-min' id='input-min' value='00'></span>"
	  		);

	  	var $confirm_row = $( ".alarm-confirm-div" );
	  	$confirm_row.html("Save");
		 
		 	$confirm_row.click(function() {
		 		$alert.modal('hide');
		 	});
		});

		// $alert.on('hide.bs.modal', function() {
  	//   console.log("model goes away now!")
  	// });

		$("#footer-bed-div").click(function() {
			var $alert = $('.bed-modal');
			$alert.modal('show');
	  	$alert.css('display', 'block');

	  	// fill in the set timing 
	  	var $set_row = $( ".dim-set-div" );

	  	// added the input boxes
	  	$set_row.html("Dimming in <span>10 min</span>...");

	  	var $confirm_row = $( ".dim-confirm-div" );
	  	$confirm_row.html("OK");
		 
		 	$confirm_row.click(function() {
		 		$alert.modal('hide');
		 	});
		});
	});
