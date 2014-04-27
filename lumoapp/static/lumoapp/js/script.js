$(function() {
  var IP_ADDRESS = '192.168.1.140';

  var $alert = $('.alert');
  var intervals = [];

  checkForNotifications();
  setInterval(checkForNotifications, 30000);

  function notifyWithLights(notificationId) {
    var notification = $('*[data-id=' + notificationId + ']');
    var description = notification.find('.event-description-div').html();
    var time = notification.find('.event-time-div').html();
    $alert.find('.description').html(description);
    $alert.find('.time').html(time);

    if ($alert.css('display') !== 'none') {
      createLightsPattern();
    }
  }

  function createLightsPattern() {
    var interval = setInterval(function() {
      changeLightsOfAll(true, 100, 200, 20000);
    }, 6000);
    intervals.push(interval);

    setTimeout(function() {
      var interval = setInterval(function() {
        changeLightsOfAll(true, 100, 255, 65535);
      }, 6000);
      intervals.push(interval);
    }, 3000);

    // var interval = setInterval(function() {
    //   changeLights(true, 255, 255, 5000, 1);
    //   changeLights(true, 255, 255, 5000, 2);
    // }, 2000);
    // intervals.push(interval);

    // interval = setInterval(function() {
    //   changeLights(true, 0, 255, 5000, 1);
    //   changeLights(true, 0, 255, 5000, 2);
    // }, 4000);
    // intervals.push(interval);

    // interval = setInterval(function() {
    //   changeLights(true, 100, 100, 25000, 3);
    // }, 3000);
    // intervals.push(interval);

    // interval = setInterval(function() {
    //   changeLights(true, 0, 100, 25000, 3);
    // }, 6000);
    // intervals.push(interval);
  }

  function changeLights(isOn, saturation, brightness, hue_value, light) {
    $.ajax({
      url: 'http://' + IP_ADDRESS + '/api/newdeveloper/lights/' + light + '/state',
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

  function changeLightsOfAll(isOn, saturation, brightness, hue_value) {
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

  function checkForNotifications() {
    $.ajax({
      url: 'check-for-notifications/'
    }).done(function(notificationId) {
      if (notificationId) {
        $alert.modal('show');
        $alert.css('display', 'block');
        notifyWithLights(notificationId);
        var lightsNotification = setInterval(function() { notifyWithLights(notificationId); }, 10000);

        $alert.on('hide.bs.modal', function() {
          clearInterval(lightsNotification);
          intervals.forEach(function(interval) {
            clearInterval(interval);
          });
          intervals = []
          // deleteAllSchedules();
          changeLightsOfAll(true, 0, 255, 65535);
          setTimeout(function() { changeLightsOfAll(true, 0, 255, 65535); }, 2000);
          setTimeout(function() { changeLightsOfAll(true, 0, 255, 65535); }, 4000);          
        });

        notifyWithLights(notificationId);
        tellAppNotificationOccurred(notificationId);
      }
    });
  }

  function tellAppNotificationOccurred(notificationId) {
    $.ajax({
      url: 'notification-occurred/' + notificationId + '/',
      type: 'GET'
    });
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
