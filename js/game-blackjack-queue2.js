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

function getGameID(user_id) {
  /* Get: https://deckdealer.hopto.org/get/players2/user_id/{ID#} */
  var url = new URL('/get/players2/user_id/' + user_id, api_url).toString();
  var temp_id = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_id = response.game_id;
    }
  });
  return temp_id;
}

function getMinPlayers(game_id) {
  /* Get: https://deckdealer.hopto.org/get/games/game_id/{ID#} */
  var url = new URL('/get/games/game_id/' + game_id, api_url).toString();
  var temp_min = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_min = parseInt(response.min_players);
    }
  });
  return temp_min;
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
        '<div class="col-1 bg-light ps-3 text-center border" style="--bs-bg-opacity: .6;">' +
          '<h3>' + player.player_id +'</h3>' +
        '</div>' +
        '<div class="col-3 bg-light ps-3 border" style="--bs-bg-opacity: .7;">' +
          '<h3>' + player.name +'</h3>' +
        '</div>' +
        '<div class="col-4 bg-light ps-3 border" style="--bs-bg-opacity: .8;">' +
          '<h3>' + player.email +'</h3>' +
        '</div>' +
      '</div>'
    )
  }

}

$(document).ready(function() {
  /* local variables */
  user_id = getUserID();
  game_id = getGameID();
  player_list = getPlayerList();
  min_players = getMinPlayers();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.table(player_list);

  /* generate HTML */
  printPlayerList(player_list);
});
