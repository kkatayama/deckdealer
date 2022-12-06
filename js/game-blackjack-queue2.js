///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
var user_id = "";
var player_list = [];

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function getUserID() {
  /* GET: https://deckdealer.hopto.org/status */
  var url = new URL('/status', api_url).toString();
  var temp_id = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_id = response.user_id;
    }
  });
  return temp_id;
}

function getPlayerList() {
  /* GET: https://deckdealer.hopto.org/get/players2 */
  var url = new URL('/get/players2', api_url).toString();
  var temp_list = [];
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      if ((response.message.includes("0")) && (response.message.includes("entries"))) {
        console.log('No registered players!');
      } else if ((response.message.includes("1")) && (response.message.includes("entry"))) {
        temp_list = [response.data];
      } else {
        temp_list = response.data;
      }
    }
  });
  return temp_list;
}

function printPlayerList(player_list) {
  for (var i = 0; i < player_list.length; i++) {
    var player = player_list[i];
    $('#player-list').append(
      '<div class="col-2">' +
        '<h2>' + player.player_id +'</h2>' +
      '</div>' +
      '<div class="col-4">' +
        '<h2>' + player.name +'</h2>' +
      '</div>' +
      '<div class="col-6">' +
        '<h2>' + player.email +'</h2>' +
      '</div>' +
    )
  }
}

$(document).ready(function() {
  /* local variables */
  user_id   = getUserID();
  player_list = getPlayerList();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.table(player_list);

  /* generate HTML */
  // printGameList(game_list);
});
