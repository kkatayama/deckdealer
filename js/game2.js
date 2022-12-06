$(document).ready(function() {
  var api_url = "https://deckdealer.hopto.org"
  var user_id = "";

  function getUserID() {
    var url = new URL('/status', api_url).toString();
    $.get(url).done(function(data) {
      user_id = data.user_id;
      console.log('user_id = ' + user_id);
      return user_id
    })
  }
  var uid = getUserID();
  console.log('uid = ' + uid);
});
