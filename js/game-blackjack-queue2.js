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
var num_players = 0;
var waiting = true;
var timer = 0;

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
  player_list = getPlayerList();

  if (!!(num_players === player_list.length)) {
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
      $('#status').html(
        '<div class="d-grid">' +
          '<button class="btn btn-primary">Start Game</button>' +
        '</div>'
      )
    }
  } else {
    num_players = player_list.length;
  }
}

function playGame(status) {
  if (status === 0) {
    window.location.href = "game-blackjack-play2.html";
  }
}

function clearTimer() {
  clearInterval(timer);
  return 0;
}

$(document).ready(function() {
  /* set variables */
  html = $('#player-list').html();
  user_id = getUserID();
  game_id = getGameID();
  min_players = getMinPlayers();
  player_list = getPlayerList();
  // num_players = player_list.length;

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.log('game_id = ' + game_id);
  console.log('min_players = ' + min_players);


  /* generate HTML: every 500 ms */
  $('#status').click(function(elem) { waiting = false; })
  timer = setInterval(function() {
    if (waiting) {
      printPlayerList()
    } else {
      playGame(clearTimer());
    }
  }, 1000);
});
