///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
var user_id = "";
var game_list = [];

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function getUserID() {
  /* GET: https://deckdealer.hopto.org/status */
  var url = new URL('/status', api_url).toString();
  var temp_id = "";
  $.ajax({url: url, type: 'get', async: false,
    success: function(response) {
      temp_id = response.user_id;
    }
  });
  return temp_id;
}

function getGameList() {
  /* GET: https://deckdealer.hopto.org/get/games */
  var url = new URL('/get/games', api_url).toString();
  var temp_list = [];
  $.ajax({url: url, type: 'get', async: false,
    success: function(response) {
      if (response.message === "1 game entry found") {
        temp_list = [response.data];
      } else {
        temp_list = response.data;
      }
    }
  });
  return temp_list;
}

function printGameList(game_list) {

}

$(document).ready(function() {
  /* local variables */
  user_id   = getUserID();
  game_list = getGameList();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.table(game_list);

  /* generate HTML */
});
