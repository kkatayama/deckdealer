var api_url = "https://deckdealer.hopto.org"

var user_id = "";
var game_id = "";
var name    = "";
var email   = "";

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
  var urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('game_id');
}

$(document).ready(function() {
  user_id = getUserID();
  game_id = getGameID();

  console.log('user_id = ' + user_id);
  console.log('game_id = ' + game_id);

  $('#game-register').submit(function(elem) {
    elem.preventDefault();

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
