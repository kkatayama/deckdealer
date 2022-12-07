///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
var html = "";
var user_id = "";
var user_name = "";
var players = [];
var active = [];
var card_index = 0;
var player_index = 1;

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function showPopup(message) {
  $('#popup').find('button').addClass('disabled')
  $('#popup').modal({backdrop: 'static', keyboard: false});
  $('#message').html("Error Processing Params:");
  $('#message-body').html(message);
  $('#popup').modal("show");
}

function hidePopup() {
  $('#popup').modal('hide');
}

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

function getUserName() {
  /* GET: https://deckdealer.hopto.org/get/users/user_id/{ID#} */
  var url = new URL('/get/users/user_id/' + user_id, api_url).toString();
  var temp_name = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_name = response.data.username;
    }
  });
  return temp_name;
}

function getPlayers() {
  /* GET: https://deckdealer.hopto.org/get/players2 */
  var url = new URL('/get/players2', api_url).toString();
  var temp_players = [];
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_players = response.data;
    }
  });
  return temp_players;
}

function getPlayerID() {
  for (var i = 0; i < players.length; i++) {
    if (players[i].user_id == user_id) {
      return players[i].player_id;
    }
  }
}

function getPlayerName() {
  for (var i = 0; i < players.length; i++) {
    if (players[i].user_id == user_id) {
      return players[i].name;
    }
  }
}

function getActiveGame() {
  /* Get: https://deckdealer.hopto.org/get/active_game2 */
  var url = new URL('/get/active_game2', api_url).toString();
  var temp_active = []
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      if ((response.message.includes("0")) && (response.message.includes("entries"))) {
        console.log('Waiting the for dealer to start...');
        temp_active = [];
      } else if ((response.message.includes("1")) && (response.message.includes("entry"))) {
        temp_active = [response.data];
      } else {
        temp_active = response.data;
      }
    }
  });
  return temp_active;
}

function printActiveGame() {
  active_game = getActiveGame();

  if (active_game.length) {
    hidePopup();
    console.log('Game is Active !')
  } else {
    showPopup("Waiting for the dealer to start...");
  }
}

function printPlayerList() {
  player_list = getPlayerList();

  if ((num_players < player_list.length) || (num_players > player_list.length)) {
    num_players = player_list.length;
    $('#game-queue').text(game_name + ' Player Queue');
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
      $('#status').removeClass('bg-light');
      $('#status').removeClass('border');
      $('#status').removeClass('rounded');
      $('#status').html(
        '<div class="btn btn-primary form-control btn-block">Start Game</div>'
      )
    }
  }
}


$(document).ready(function() {
  /* set variables */
  html = $('#player-list').html();
  user_id = getUserID();
  players = getPlayers();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.log('=== players ===')
  console.table(players);

  /* generate HTML: every 500 ms */
  // var timer = setInterval(function() { printPlayerList() }, 1000);
  $('#status').click(function(elem) {
    clearInterval(timer);
    window.location.href = "game-blackjack-play2.html";
  });

  printActiveGame();

});
