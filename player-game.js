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
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_id = response.user_id;
    }
  });
  return temp_id;
}
/* */
function getGameList() {
  /* GET: https://deckdealer.hopto.org/get/games */
  var url = new URL('/get/games', api_url).toString();
  var temp_list = [];
  $.ajax({url: url, type: 'GET', async: false,
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
  for (var i = 0; i < game_list.length; i++) {
    var game = game_list[i];
    $('#game-list').append(
      '<div class="accordion-item">' +
        '<h2 class="accordion-header" id="game-' + game.game_id +'">' +
          '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-game-' + game.game_id + '" aria-expanded="true" aria-controls="collapse-game-"' + game.game_id +'" >' +
            game.name +
          '</button>' +
        '</h2>' +
        '<div id="collapse-game-' + game.game_id + '" class="accordion-collapse collapse" aria-labelledby="game-' + game.game_id + '" data-bs-parent="#game-list">' +
          '<div class="accordion-body">' +
            'min_players = ' + game.min_players + '<br />' +
            'max_players = ' + game.max_players + '<br />' +
            'min_decks = ' + game.min_decks + '<br />' +
            'max_decks = ' + game.max_decks + '<br />' +
            'player_actions = ' + game.player_actions + '<br />' +
            '<br /><strong>RULES</strong><br />' +
            game.rules.replaceAll(',', '<br />') + '<br />' +
            '<div class="d-grid py-3">' +
            '<a class="btn btn-primary" href="game-register2.html?game_id=' + game.game_id + '">Play ' + game.name + '</a>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>'
    )
  }
}

$(document).ready(function() {
  /* local variables */
  user_id   = getUserID();
  game_list = getGameList();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.table(game_list);

  /* generate HTML */
  printGameList(game_list);
});
