///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"
var user_id = "";

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function getUserID() {
  var url = new URL('/status', api_url).toString();
  $.ajax({
    url: url,
    type: 'get',
    async: false,
    success: function(data) {
      user_id = data.user_id;
      console.log('user_id = ' + user_id);
    }
  });
  return user_id;
}

$(document).ready(function() {
  var uid = getUserID();
  console.log('uid = ' + uid);
});
