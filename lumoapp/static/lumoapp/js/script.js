var IP_ADDRESS = '192.168.1.140';
var intervals = [];

function changeLightsOfAll(isOn, saturation, brightness, hue_value) {
  console.log('CHANGE LIGHTS OF ALL');
  $.ajax({
    url: 'http://' + IP_ADDRESS + '/api/newdeveloper/groups/0/action',
    type: 'PUT',
    data: JSON.stringify({
      on: isOn,
      sat: saturation,
      bri: brightness,
      hue: hue_value,
      transitiontime:20
    })
  });    
}

function clearLightPatterns() {
  intervals.forEach(function(interval) {
    clearInterval(interval);
  });
  intervals = []
  // deleteAllSchedules();
  changeLightsOfAll(true, 0, 255, 65535);
  setTimeout(function() { changeLightsOfAll(true, 0, 255, 65535); }, 2000);
  setTimeout(function() { changeLightsOfAll(true, 0, 255, 65535); }, 4000);          
}

$(function() {
  var $alert = $('.alert');

  checkForNotifications();
  setInterval(checkForNotifications, 10000);

  function createEndingLightsPattern() {
    var interval = setInterval(function() {
      changeLightsOfAll(true, 100, 200, 20000);
    }, 6000);
    intervals.push(interval);

    setTimeout(function() {
      var interval = setInterval(function() {
        // Change to a red color
        changeLightsOfAll(true, 255, 255, 65000);
      }, 6000);
      intervals.push(interval);
    }, 3000);
  }

  function createStartingLightsPattern() {
    var interval = setInterval(function() {
      changeLightsOfAll(true, 255, 255, 45000);
    }, 6000);
    intervals.push(interval);

    setTimeout(function() {
      var interval = setInterval(function() {
        // Change to a green color
        changeLightsOfAll(true, 255, 255, 26000);
      }, 6000);
      intervals.push(interval);
    }, 3000);
  }

  function notifyWithLights(notification) {
    var $notification = $('*[data-id=' + notification.id + ']');
    var description = $notification.find('.event-description-div').html();
    $alert.find('.description').html(description);

    n = notification;
    console.log(notification);
    if (notification.is_end) {
      var time = $notification.find('.end-time').html();
      $alert.find('.time').html('ending at ' + time);
      if ($alert.css('display') !== 'none') {
        createEndingLightsPattern();
      }
    } else {
      var time = $notification.find('.event-time-div').html();
      $alert.find('.time').html('starting at ' + time);      
      if ($alert.css('display') !== 'none') {
        createStartingLightsPattern();
      }
    }
  }

  function changeLights(isOn, saturation, brightness, hue_value, light, transitiontime) {
    if (transitiontime === undefined) {
      transitiontime = 20;
    }
    $.ajax({
      url: 'http://' + IP_ADDRESS + '/api/newdeveloper/lights/' + light + '/state',
      type: 'PUT',
      data: JSON.stringify({
        on: isOn,
        sat: saturation,
        bri: brightness,
        hue: hue_value,
        transitiontime:transitiontime
      })
    });
  }

  function checkForNotifications() {
    $.ajax({
      url: 'check-for-notifications/'
    }).done(function(notification) {
      if (notification) {
        $alert.modal('show');
        $alert.css('display', 'block');
        notifyWithLights(notification);
        var lightsNotification = setInterval(function() { notifyWithLights(notification); }, 10000);

        $alert.on('hide.bs.modal', function() {
          clearInterval(lightsNotification);
          clearLightPatterns();
        });

        notifyWithLights(notification);
        tellAppNotificationOccurred(notification);
      }
    });
  }

  function tellAppNotificationOccurred(notification) {
    if (notification.is_end) {
      $.ajax({
        url: 'end-notification-occurred/' + notification.id + '/',
        type: 'GET'
      });
    } else {
      $.ajax({
        url: 'start-notification-occurred/' + notification.id + '/',
        type: 'GET'
      });      
    }
  }

  $('body').on('click', function() {
    if ($alert.css('display') !== 'none') {
      $alert.modal('hide');
    }
  });

  function deleteAllSchedules() {
    for (var i = 0; i < 100; i++) {
      $.ajax({
        url: 'http://' + IP_ADDRESS + '/api/newdeveloper/schedules/' + i,
        type: 'DELETE',
        async: false
      });
    }
  }
});
