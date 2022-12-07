///////////////////////////////////////////////////////////////////////////////
//                              Global Variables                             //
///////////////////////////////////////////////////////////////////////////////
var api_url = "https://deckdealer.hopto.org"

///////////////////////////////////////////////////////////////////////////////
//                      Global Variables (for debugging)                     //
///////////////////////////////////////////////////////////////////////////////
var user_id = "";
var game_id = "";
var name    = "";
var email   = "";

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
  /* TAKEN FROM: /game-register2?game_id={SOME_NUMBER}  */
  var urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('game_id');
}

$(document).ready(function() {
  /* local variables */
  user_id = getUserID();
  game_id = getGameID();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.log('game_id = ' + game_id);

  /* handle submit */
  $('#game-register').submit(function(elem) {
    elem.preventDefault();
    /* register player */
    /* POST: https://deckdealer.hopto.org/add/players2
     * PARAMS (example):
     * {
     *   user_id: "3",
     *   game_id: "1",
     *   name: "alice",
     *   email: "alice@udel.edu",
     * }
     * RETURNS:
     * {
     *   "message": "data added to <players>",
     *   "player_id": "2",
     *   "user_id": "3",
     *   "game_id": "1",
     * }
     */
    var url = new URL('/add/players2', api_url).toString();
    $.ajax({url: url, method: 'POST',
            data: {
              user_id: user_id,
              game_id: game_id,
              name:  $('#name').val(),
              email: $('#email').val(),
            },
            success: function(response) {
              console.log(response);
              window.location.href = 'game-queue2.html'
            }
           });
  });
});
