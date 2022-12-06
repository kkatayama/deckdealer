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
  var temp_id = "";
  $.ajax({
    url: url,
    type: 'get',
    async: false,
    success: function(data) {
      temp_id = data.user_id;
    }
  });
  return temp_id;
}

$(document).ready(function() {
  user_id = getUserID();
  console.log('user_id = ' + user_id);
});
