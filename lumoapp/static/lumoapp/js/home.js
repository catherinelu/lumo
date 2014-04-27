$(function() {
  checkForAlarms();
  setInterval(checkForAlarms, 30000);

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
    $(this).click( function() {
      var $end_event = $('.end-event-modal');
      $end_event.modal('show');
      $end_event.css('display', 'block');
      var $img_element = $(this).find("#event-remind-img");
      console.log($img_element.attr("src"));
      var img_src_suffix = $img_element.attr("src").slice(-12);
      console.log(img_src_suffix);
      if (img_src_suffix === "tones-20.png") {
        $end_event.find('.end-event-description').html('Aha, end of event reminder is set');
        $img_element.attr('src', '/static/lumoapp/img/bells-25.png');
      } else {
        $end_event.find('.end-event-description').html('End of event reminder cancelled');
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

  	var $confirm_row = $( ".alarm-confirm-div" );
	 
	 	$confirm_row.click(function() {
	 		var hour_entered = parseInt($set_row.find('[name="input-hour"]').val(), 10);
	 		var minutes_entered = parseInt($set_row.find('[name="input-min"]').val(), 10);
	 		$.ajax({
	 			url: 'save-alarm/' + hour_entered + '/' + minutes_entered + '/'
	 		}).done(function() {
		 		$alert.modal('hide');
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
      });	 	
    });   

	});

	function checkForAlarms() {
		console.log('checing');
    $.ajax({
      url: 'check-for-alarms/'
    }).done(function(alarmId) {
    	console.log('done');
      if (alarmId) {
      	var $alert = $('.alert');
      	$alert.find('description').html('Ring ring! It\'s your alarm!')
        $alert.modal('show');
        $alert.css('display', 'block');
        createLightsPattern();
        var lightsNotification = setInterval(function() { createLightsPattern(); }, 10000);

        $alert.on('hide.bs.modal', function() {
          clearInterval(lightsNotification);
          intervals.forEach(function(interval) {
            clearInterval(interval);
          });
          intervals = [];
          changeLightsOfAll(true, 0, 255, 65535);
          setTimeout(function() { changeLightsOfAll(true, 0, 255, 65535); }, 2000);
          setTimeout(function() { changeLightsOfAll(true, 0, 255, 65535); }, 4000);          
        });

        tellAppAlarmOccurred(alarmId);
      }
    });
  }

  function tellAppAlarmOccurred(alarmId) {
    $.ajax({
      url: 'alarm-occurred/' + alarmId + '/'
    });
  }
});
