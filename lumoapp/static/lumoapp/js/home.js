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

		var $alert = $('.alarm-modal');

		$("#footer-alarm-div").click(function() {
			$alert.find('.modal-content').empty();

			$alert.modal('show');
	  	$alert.css('display', 'block');

	  	// build the container and other divs 
	  	var $container = $( "<div class='container-fluid'/>" );
	  	var $alarm_row = $( "<div class='row alarm-set-div'/>" );
	  	var $confirm_row = $( "<div class='row alarm-confirm-div'/>" );

	  	// 
	  	$alarm_row.html("row goes here");
	  	$confirm_row.html("button goes here");

	  	$container.append($alarm_row);
	  	$container.append($confirm_row);

		  $alert.find('.modal-content').append($container);
		  
		});

		// $alert.on('hide.bs.modal', function() {
  	//   console.log("model goes away now!")
  	// });

		$("#footer-bed-div").click(function() {
			$alert.modal('show');
	  	$alert.css('display', 'block');
		  $alert.find('.modal-content').html("Bed time");
		});
	});
