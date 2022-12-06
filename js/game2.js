///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"
var user_id = "";
var uid = "";

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function getUserID() {
  var url = new URL('/status', api_url).toString();
  return $.get(url, function(data) {
    user_id = data.user_id;
    console.log('user_id = ' + user_id);
    return user_id;
  })
}

$(document).ready(function() {
  uid = getUserID();
  console.log('uid = ' + uid);
});
