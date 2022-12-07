///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
var html = "";
var user_id = "";
var game_id = "";
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

function getGameID() {
  /* Get: https://deckdealer.hopto.org/get/players2/user_id/{ID#} */
  var url = new URL('/get/players2/user_id/' + user_id, api_url).toString();
  var temp_id = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_id = response.data.game_id;
    }
  });
  return temp_id;
}

function getMinPlayers() {
  /* Get: https://deckdealer.hopto.org/get/games/game_id/{ID#} */
  var url = new URL('/get/games/game_id/' + game_id, api_url).toString();
  var temp_min = 0;
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_min = parseInt(response.data.min_players);
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

function printPlayerList() {
  var player_list = getPlayerList();

  $('#player-list').html(html);
  for (var i = 0; i < player_list.length; i++) {
    var player = player_list[i];
    $('#player-list').append(
      '<div class="row justify-content-center text-success">' +
        '<div class="col-1 bg-light ps-3 text-center border" style="--bs-bg-opacity: .6;">' +
          '<h3>' + player.player_id +'</h3>' +
        '</div>' +
        '<div class="col-3 bg-light ps-3 border" style="--bs-bg-opacity: .6;">' +
          '<h3>' + player.name +'</h3>' +
        '</div>' +
        '<div class="col-4 bg-light ps-3 border" style="--bs-bg-opacity: .6;">' +
          '<h3>' + player.email +'</h3>' +
        '</div>' +
      '</div>'
    )
  }
  if (player_list.length < min_players) {
    $('#status').html('<p class="lh-base">waiting for additional players...</p>')
  } else {
    $('#status').html('<a class="btn btn-primary btn-block" href="game-blackjack-play2.html">Start Game</a>')
    // $('#status').html('<a class="btn btn-primary btn-block" href="#">Start Game</a>')
  }
}

$(document).ready(function() {
  /* set variables */
  html = $('#player-list').html();
  user_id = getUserID();
  game_id = getGameID();
  min_players = getMinPlayers();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.log('game_id = ' + game_id);
  console.log('min_players = ' + min_players);

  /* generate HTML: every 500 ms */
  var interval = setInterval(function() { printPlayerList() }, 500);
  $('#status').click(function(elem) {
    clearInterval(interval);
  })
});
