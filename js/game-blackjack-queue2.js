///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
var user_id = "";
var game_id = "";
var player_list = [];
var min_players = 0;

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
      '<div class="row justify-content-center text-success">' +
        '<div class="col-1 ps-3 text-center border">' +
          '<h3>' + player.player_id +'</h3>' +
        '</div>' +
        '<div class="col-3 ps-3 border">' +
          '<h3>' + player.name +'</h3>' +
        '</div>' +
        '<div class="col-4 ps-3 border">' +
          '<h3>' + player.email +'</h3>' +
        '</div>' +
      '</div>'
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
  printPlayerList(player_list);
});
