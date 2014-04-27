$(function() {
  var IP_ADDRESS = '192.168.1.140';

  var $alert = $('.alert');
  $alert.modal();

  $alert.modal('show');
  $alert.css('display', 'block');

  // checkForNotifications();

  notifyWithLights('1');

  function notifyWithLights(notificationId) {
    var notification = $('*[data-id=' + notificationId + ']');
    $alert.find('.modal-content').html(notification.find('.event-description-div').html());

    if ($alert.css('display') !== 'none') {
      setTimeout(function() {
        changeLights(true, 255, 255, 10000);
      }, 3000);
      setTimeout(function() {
        changeLights(true, 100, 100, 5000);
      }, 3000);
      setTimeout(notifyWithLights, notification, 1000);
    }
  }

  function changeLights(isOn, saturation, brightness, hue_value) {
    for (var i = 1; i <= 3; i++) {
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
      }
    });

    setTimeout(checkForNotifications, 30000);
  }

});
