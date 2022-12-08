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

var timer = 0;

/* taken from: https://stackoverflow.com/questions/18673860/defining-a-html-template-to-append-using-jquery */
var player_template = ({ num_cols, info, cards }) => `
<div class="row row-cols-${num_cols} justify-content-center mt-2">${info}${cards}</div>
`;

var player_info_template = ({ player_id, player_name, score }) => `
  <div class="col-auto">
    <div class="card" id="card_${player_id}">
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

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////
function renderPlayerTemplate(player, cards, num_cols=6) {
  var score = getPlayerScore(cards);
  var images = [];
  for (var i = 0; i < cards.length; i++) {
    if (i === 1) {
      if (player.name === "dealer") {
        images[i] = {img: "back.png"};
        score = "??";
      } else {
        images[i] = {img: cards[i].player_hand + ".png"};
      }
    } else {
      images[i] = {img: cards[i].player_hand + ".png"};
    }
  }

  var html_info = [{ player_id: player.player_id, player_name: player.name, score: score }].map(player_info_template).join('');
  var html_cards = images.map(player_cards_template).join('');
  var html_player = [{ num_cols: num_cols, info: html_info, cards: html_cards }].map(player_template).join('');
  // console.log(html_player);
  return html_player;
}

function renderPlayerTemplateAll(player, cards, num_cols=6) {
  var score = getPlayerScore(cards);
  var images = [];
  for (var i = 0; i < cards.length; i++) {
      images[i] = {img: cards[i].player_hand + ".png"};
  }

  var html_info = [{ player_id: player.player_id, player_name: player.name, score: score }].map(player_info_template).join('');
  var html_cards = images.map(player_cards_template).join('');
  var html_player = [{ num_cols: num_cols, info: html_info, cards: html_cards }].map(player_template).join('');
  // console.log(html_player);

  return html_player;
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

function getPlayerNameByID(p_id) {
  for (var i = 0; i < players.length; i++) {
    if (players[i].player_id == p_id) {
      return players[i].name;
    }
  }
}

function getPlayerCards(player) {
  /*
   * POST: https://deckdealer.hopto.org/get/active_game2
   * PARAMS: (example):
   * {
   *   filter: `(player_id = 1 AND player_action != "stay")`
   * }
   */
  var url = new URL('/get/active_game2', api_url).toString();
  var temp_cards = [];
  $.ajax({url: url, type: 'POST', async: false,
    data: {
      filter: `(player_id = ${player.player_id} AND player_action != "stay")`,
    },
    success: function(response) {
      temp_cards = response.data;
    }
  });
  return temp_cards;
}

function getPlayerScore(cards) {
  var temp_score = 0
  for (var i = 0; i < cards.length; i++) {
    var card = cards[i].player_hand;
    if (parseInt(card)) {
      temp_score = temp_score + parseInt(card);
    } else {
      if ((card.includes('J')) || (card.includes('Q')) || (card.includes('K'))) {
        temp_score = temp_score + 10;
      } else {
        /* card is an ACE */
        if ((temp_score + 11) > 21) {
          temp_score = temp_score + 1;
        } else {
          temp_score = temp_score + 11;
        }
      }
    }
  }
  return temp_score;
}

function getActiveGame() {
  /* Get: https://deckdealer.hopto.org/get/active_game2 */
  var url = new URL('/get/active_game2', api_url).toString();
  var temp_active = [];
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      if ((response.message.includes("found 0")) && (response.message.includes("entries"))) {
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

function getFinishedPlayers() {
  var url = new URL('/get/active_game2', api_url).toString();
  var temp_players = [];
  $.ajax({url: url, type: 'POST', async: false,
    data: {
      filter: `(player_action = "stay") GROUP BY (player_id) ORDER BY (entry_id)`,
    },
    success: function(response) {
      if (response.data.length === 0) {
        temp_players = [];
      } else if ((response.message.includes("1")) && (response.message.includes("entry"))) {
        temp_players = [response.data];
      }
        else {
        temp_players = response.data;
      }
    }
  });
  return temp_players;
}

function getRemainingPlayers(){
  var url = new URL('/get/active_game2', api_url).toString();
  var temp_players = [];
  var finished_players = getFinishedPlayers();


  if (finished_players.length) {
    var filter_template = ({ player_id }) => `player_id != ${player_id}`
    var temp_filter = finished_players.map(filter_template).join(' AND ');
    console.log ('=== TEMP FILTER ===');
    console.log(temp_filter)

    $.ajax({
      url: url, type: 'POST', async: false,
      data: {
        filter: `(player_action = "setup" AND ${temp_filter}) GROUP BY (player_id) ORDER BY (entry_id)`,
      },
      success: function(response) {
        if ((response.message.includes("found 0")) && (response.message.includes("entries"))) {
          temp_players = [];
        } else if ((response.message.includes("1")) && (response.message.includes("entry"))) {
          temp_players = [response.data];
        } else {
          temp_players = response.data;
        }
      }
    });
  } else {
    $.ajax({
      url: url, type: 'POST', async: false,
      data: {
        filter: `(player_action = "setup") GROUP BY (player_id) ORDER BY (entry_id)`,
      },
      success: function(response) {
        if ((response.message.includes("found 0")) && (response.message.includes("entries"))) {
          temp_players = [];
        } else if ((response.message.includes("1")) && (response.message.includes("entry"))) {
          temp_players = [response.data];
        } else {
          temp_players = response.data;
        }
      }
    });
  }
  return temp_players;
}

function showActiveGame() {
  active_game = getActiveGame();

  if (active_game.length) {
    remaining_players = getRemainingPlayers();

    $('#players').html('');
    for (var i = 0; i < players.length; i++) {
      var player = players[i];
      var cards = getPlayerCards(player);
      var num_cols = (cards.length > 4) ? 8 : 6;
      if (remaining_players.length > 1) {
        $('#players').append(renderPlayerTemplate(player, cards, num_cols));
      } else {
        $('#players').append(renderPlayerTemplateAll(player, cards, num_cols));
        players[i]["score"] = getPlayerScore(cards);
      }
    }
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

  $('#game-play').html('Blackjack: (' + player_name + ')');

  /* generate HTML: every 500 ms */
  // var timer = setInterval(function() { printPlayerList() }, 1000);
  $('#status').click(function(elem) {
    clearInterval(timer);
    window.location.href = "game-blackjack-play2.html";
  });

  showActiveGame();

});
