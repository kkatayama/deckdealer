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
var player_id = "";
var player_name = "";

var active = [];
var card_index = 1;

/* taken from: https://stackoverflow.com/questions/18673860/defining-a-html-template-to-append-using-jquery */
var player_template = ({ num_cols, info, cards }) => `
<div class="row row-cols-${num_cols} justify-items-center mt-2">${info}${cards}</div>
`;

var player_info_template = ({ player_id, player_name, score }) => `
  <div class="col-auto">
    <div class="card">
      <h5 class="card-header" id="header_${player_id}">${player_name}</h5>
      <div class="card-body">
        <h5 class="card-title" id="score_${player_id}">score: ${score}</h5>
      </div>
    </div>
  </div>
`;

var player_cards_template = ({ img }) => `
  <div class="col"><img src="${img}" class="img-fluid"></div>
`;

var msg_body_template = ({ msg }) => `
<div class="d-flex align-items-center">
  <strong>${msg}</strong>
  <div class="spinner-border ms-auto" role="status" aria-hidden="true">
  </div>
</div>
`;

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function renderPlayerTemplate() {
  num_cols = (num_cards > 4) ? 8 : 6;
  var html_info = [{ player_id: "2", user_name: "alice", score: 20 },].map(player_info_template).join('');
  var html_cards = [{ img: "6S.png" }, { img: "6H.png" }].map(player_cards_template).join('');
  var html_player = [{ num_cols: 6, info: html_info, cards: html_cards }].map(player_template).join('');
  $('#players').append(html_player);
}

function renderMsgBodyTemplate(msg) {
  return [{ msg: msg }].map(msg_body_template).join('');
}

function showPopup(message='', kind="alert") {
  /* disable close button and keyboard escape */
  $('#message-title').find('button').addClass('disabled')
  $('#popup').modal({backdrop: 'static', keyboard: false});

  if (kind === "alert") {
    $('#message-header').addClass('d-none');
    $('#message-footer').addClass('d-none');
  }
  if (kind === "action"){
    $('#message-header').removeClass('d-none');
    $('#message-footer').removeClass('d-none');
    if (user_name === "dealer") {
      $('#message-title').html('Dealer Action');
      $('#player_action').addClass('d-none');
      $('#dealer_setup').removeClass('d-none');
    } else {
      $('#message-title').html('Player Action');
      $('#player_action').removeClass('d-none');
      $('#dealer_setup').addClass('d-none');
    }
  }
  $('#message-body').html(renderMsgBodyTemplate(message));

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


function dealCard() {
  /* GET: https://deckdealer.hopto.org/get/deck?filter=(card_id={card_index}) */
  var url = new URL('/get/deck?filter=(card_id=' + card_index + ')', api_url).toString();
  var temp_card = {};
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_card = response.data;
      card_index++;
    }
  });
  return temp_card;
}

function getActiveGame() {
  /* Get: https://deckdealer.hopto.org/get/active_game2 */
  var url = new URL('/get/active_game2', api_url).toString();
  var temp_active = [];
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
    console.log('Game is Active !');

    showPopup('What would you like to do?', 'action')
  } else {
    showPopup('Waiting for the dealer to start...');

    //showPopup('Click SETUP to deal the first round of cards', 'action');
  }
}


$(document).ready(function() {
  /* set variables */
  html = $('#player-list').html();
  user_id   = getUserID();
  user_name = getUserName();

  players     = getPlayers();
  player_id   = getPlayerID();
  player_name = getPlayerName();

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
