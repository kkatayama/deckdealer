var api_url = "https://deckdealer.hopto.org"
/*Is there a bug?*/
var html = "";
var user_id = "";
var game_id = "";
var game_name = "";
var min_players = 0;
var num_players = 0;

function getUserID() {
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
  var url = new URL('/get/players/user_id/' + user_id, api_url).toString();
  var temp_id = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_id   = response.data.game_id;
    }
  });
  return temp_id;
}

function getGameInfo() {
  /* Get: https://deckdealer.hopto.org/get/games/game_id/{ID#} */
  var url = new URL('/get/games/game_id/' + game_id, api_url).toString();
  var min  = 0;
  var name = "";
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      min = parseInt(response.data.min_players);
      name = response.data.name;
    }
  });
  return {min, name}
}


function getPlayerList() {
  var url = new URL('/get/players', api_url).toString();
  var temp_list = []
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
  game_id = getGameID();
  game_info = getGameInfo();
  game_name = game_info.name;
  min_players = game_info.min;
  player_list = getPlayerList();
  // num_players = player_list.length;

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.log('game_id = ' + game_id);
  console.log('min_players = ' + min_players);


  /* generate HTML: every 500 ms */
  var timer = setInterval(function() { printPlayerList() }, 1000);
  $('#status').click(function(elem) {
    clearInterval(timer);
    window.location.href = "game-blackjack.html";
  });

});
