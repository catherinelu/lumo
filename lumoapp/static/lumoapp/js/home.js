$(function() {
	var ALARM_PNG = 'static/lumoapp/img/alarm-25.png';
	var GREEN_ALARM_PNG = 'static/lumoapp/img/alarm-25-green.png';

  checkForAlarms();
  setInterval(checkForAlarms, 10000);

	$( ".event-entry-overview" ).click(function() {
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
  	var text = $( this ).text();
  	if (text.length > 18) {
  		$(this).html(text.substr(0, 18) + '...')
  	}
	});

  $( ".event-detail-location-div" ).each(function( index ) {
  	var text = $( this ).text();
  	if (text.length > 0) {
  		$(this).html('@' + text)
  	}
	});


  $(".event-detail-remind-div").each(function( index ) {
    $(this).click( function(event) {
    	var $currentTarget = $(event.currentTarget);
    	var eventId = $currentTarget.parents('.event-entry-div').attr('data-id');

      var $end_event = $('.end-event-modal');
      $end_event.modal('show');
      $end_event.css('display', 'block');

      var $img_element = $(this).find("#event-remind-img");
      var img_src_suffix = $img_element.attr("src").slice(-12);

      if (img_src_suffix === "tones-20.png") {
        $end_event.find('.end-event-description').html('An end of event reminder is set');

        $.ajax({
        	url: 'set-end-event-reminder/' + eventId + '/'
        });

        $img_element.attr('src', '/static/lumoapp/img/bells-25.png');
      } else {
        $end_event.find('.end-event-description').html('Your end of event reminder is cancelled');

        $.ajax({
        	url: 'cancel-end-event-reminder/' + eventId + '/'
        });

        $img_element.attr('src', '/static/lumoapp/img/tones-20.png');
      }
      setTimeout(function() { $end_event.modal('hide'); }, 3000);
    });
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

    $(".average-sleeptime-div").html("7h 23min of sleep on average last week!");

  	var $confirm_row = $( ".alarm-confirm-div" );
	 
	 	$confirm_row.click(function() {
	 		var hour_entered = parseInt($set_row.find('[name="input-hour"]').val(), 10);
	 		var minutes_entered = parseInt($set_row.find('[name="input-min"]').val(), 10);
	 		$.ajax({
	 			url: 'save-alarm/' + hour_entered + '/' + minutes_entered + '/'
	 		}).done(function() {
		 		$alert.modal('hide');
		 		$('#footer-alarm-div img').attr('src', GREEN_ALARM_PNG);
	 		});
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

   // added the input boxes
    $set_row.html("Dimming in &nbsp; <span class='alarm-time-span'> \
      <input class='time-input-div' type='number' min='1' max='30' name='input-dim' id='input-dim' value='10'></span> min..."
    );

  	var $confirm_row = $( ".dim-confirm-div" );
  	$confirm_row.html("OK");
	 
	 	$confirm_row.click(function() {
      var minutes_entered = parseInt($set_row.find('[name="input-dim"]').val(), 10);
      $.ajax({
        url: 'save-dim/' + minutes_entered + '/'
      }).done(function() {
        $alert.modal('hide');
        dimLights(minutes_entered);
      });	 	
    });   

	});

	function checkForAlarms() {
    $.ajax({
      url: 'check-for-alarms/'
    }).done(function(alarm) {
      if (alarm) {
      	var $alert = $('.alert');
      	$alert.find('.description').html('Time to wake up!');
      	$alert.find('.time').html(alarm.time)
        $alert.modal('show');
        $alert.css('display', 'block');
        brightenLights();

        $alert.on('hide.bs.modal', function() {
          $('#footer-alarm-div img').attr('src', ALARM_PNG);
        });

        tellAppAlarmOccurred(alarm.id);
      }
    });
  }

  function tellAppAlarmOccurred(alarmId) {
    $.ajax({
      url: 'alarm-occurred/' + alarmId + '/'
    });
  }

  function dimLights(minutes) {
  	// settings lights to be bright at the beginning
  	changeLightsOfAll(true, 0, 255, 0);
  	// dimmming
  	setTimeout(function() { changeLightsOfAll(true, 0, 0, 0, 10 * 60 * minutes); }, 3000);
  	// turning off
  	setTimeout(function() { changeLightsOfAll(false, 0, 0, 0); }, 5000);
  }

  function brightenLights() {
  	// settings lights to be dim at the beginning
  	changeLightsOfAll(true, 0, 0, 0);
  	// brightening, taking 1 minute
  	setTimeout(function() { changeLightsOfAll(true, 0, 255, 0, 10 * 60); }, 3000);
  }
});
