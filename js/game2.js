///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
// var user_id = "";
// var game_list = [];

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function getUserID() {
  /* GET: https://deckdealer.hopto.org/status */
  var url = new URL('/status', api_url).toString();
  var temp_id = "";
  $.ajax({url: url, type: 'get', async: false,
    success: function(data) {
      temp_id = data.user_id;
    }
  });
  return temp_id;
}

function getGameList() {
  /* GET: https://deckdealer.hopto.org/get/games */
  var url = new URL('/get/games', api_url).toString();
  var temp_list = [];
  $.ajax({url: url, type: 'get', async: false,
    success: function(data) {
      temp_list = data.data;
    }
  });
  return temp_list;
}

$(document).ready(function() {
  var user_id   = getUserID();
  var game_list = getGameList();
  console.log('user_id = ' + user_id);
  console.table(game_list);
});
