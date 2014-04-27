$(function() {
  var IP_ADDRESS = '192.168.1.140';

  var $alert = $('.alert');
  $alert.modal();

  $alert.modal('show');
  $alert.css('display', 'block');

  // checkForNotifications();

  function notifyWithLights(notificationId) {
    var notification = $('*[data-id=' + notificationId + ']');
    var description = notification.find('.event-description-div').html();
    var time = notification.find('')
    $alert.find('.modal-content').html(description);

    if ($alert.css('display') !== 'none') {
      setTimeout(function() {
        changeLights(true, 255, 255, 10000);
      }, 3000);
      setTimeout(function() {
        changeLights(true, 100, 100, 5000);
      }, 6000);
    }
  }

  function changeLights(isOn, saturation, brightness, hue_value) {
    for (var i = 1; i <= 3; i++) {
      console.log('calling changeLights ' + i);
      $.ajax({
        url: 'http://' + IP_ADDRESS + '/api/newdeveloper/lights/' + i + '/state',
        type: 'PUT',
        data: JSON.stringify({
          on: isOn,
          sat: saturation,
          bri: brightness,
          hue: hue_value
        })
      });
    }
  }

  function checkForNotifications() {
    $.ajax({
      url: 'check-for-notifications/'
    }).done(function(notificationId) {
      if (notificationId) {
        notifyWithLights(notificationId);
        var lightsNotification = setInterval(function() { notifyWithLights(notificationId); }, 10000);

        $alert.on('hide.bs.modal', function() {
          clearInterval(lightsNotification);
        });

        notifyWithLights(notificationId);
        tellAppNotificationOccurred(notificationId);
      }
    });

    setTimeout(checkForNotifications, 30000);
  }

  function tellAppNotificationOccurred(notificationId) {
    $.ajax({
      url: 'notification-occurred/' + notificationId + '/',
      type: 'POST'
    });
  }

});
