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
var spectators = [];

var active = [];
var card_index = 1;
var remaining_players = [];

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

var alert_body_template = ({ msg }) => `
<div class="d-flex align-items-center">
  <strong>${msg}</strong>
  <div class="spinner-border ms-auto" role="status" aria-hidden="true">
  </div>
</div>
`;

var action_body_template = ({ msg }) => `
<div class="d-flex align-items-center">
  <strong>${msg}</strong>
</div>
`;

///////////////////////////////////////////////////////////////////////////////
//                              Global Functions                             //
///////////////////////////////////////////////////////////////////////////////

function renderAlertBodyTemplate(msg) {
  return [{ msg: msg }].map(alert_body_template).join('');
}

function renderActionBodyTemplate(msg) {
  return [{ msg: msg }].map(action_body_template).join('');
}

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

function showPopup(message, kind="alert") {
  /* disable close button and keyboard escape */
  $('#message-header').find('button').addClass('disabled')
  $('#popup').modal({backdrop: 'static', keyboard: false});

  if (kind === "setup") {
    $('#message-header').removeClass('d-none');
    $('#message-footer').removeClass('d-none');
    $('#message-title').html('Dealer Action');
    $('#player-action').addClass('d-none');
    $('#dealer-setup').removeClass('d-none');
    $('#message-body').html(renderActionBodyTemplate(message));
  } else if (kind === "alert") {
    $('#message-header').addClass('d-none');
    $('#message-footer').addClass('d-none');
    $('#message-body').html(renderAlertBodyTemplate(message));
  } else if (kind === "action"){
    $('#message-header').removeClass('d-none');
    $('#message-footer').removeClass('d-none');
    $('#message-title').html('Player Action');
    $('#player-action').removeClass('d-none');
    $('#dealer-setup').addClass('d-none');
    $('#message-body').html(renderActionBodyTemplate(message));
  } else if (kind === "close") {
    $('#message-header').removeClass('d-none');
    $('#message-footer').removeClass('d-none');
    $('#message-title').html('Dealer Action');
    $('#player-action').addClass('d-none');
    $('#dealer-setup').addClass('d-none');
    $('#dealer-close').removeClass('d-none');
    $('#message-body').html(renderActionBodyTemplate(message));
  }

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

function getSpectators() {
  /* GET: https://deckdealer.hopto.org/get/spectators2 */
  var url = new URL('/get/spectators2', api_url).toString();
  var temp_spectators = [];
  $.ajax({url: url, type: 'GET', async: false,
    success: function(response) {
      temp_spectators = response.data;
    }
  });
  return temp_spectators;
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

function cardValue(card) {

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

function addActiveGame(player, card, action) {
  /*
   * POST: https://deckdealer.hopto.org/add/active_game2
   * PARAMS (example):
   * {
   *   game_id: "1",
   *   user_id: "4",
   *   player_id: "3",
   *   player_hand: "4H",
   *   player_action: "setup",
   * }
   */

  var url = new URL('/add/active_game2', api_url).toString();
  $.ajax({url: url, type: 'POST', async: false,
    data: {
      game_id: player.game_id,
      user_id: player.user_id,
      player_id: player.player_id,
      player_hand: card.key,
      player_action: action,
    },
    success: function(response) {
      console.log(response);
    }
  });
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
    var filter_template = ({ player_id }) => `player_id != ${player_id}`;
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
    startTimer();
    hidePopup();
    card_index = active_game.length + 1;
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
        players[i]["winner"] = false;
      }
    }

    if (remaining_players.length) {
      var player = remaining_players[0];

      var temp_name = getPlayerNameByID(player.player_id);
      if (temp_name === player_name) {
        showPopup(`Player Turn: (${temp_name})`, 'action');
        $('#hit').click(function(elem) {
          hidePopup();
          addActiveGame(player, card=dealCard(), 'hit');
          // setTimeout(function() { showActiveGame() }, 5000);
        });
        $('#stay').click(function(elem) {
          hidePopup();
          addActiveGame(player, card={key: 0}, 'stay');
          // setTimeout(function() { showActiveGame() }, 5000);
        });
      } else {
        showPopup(`Player Turn: (${temp_name})`, 'alert');
      }
    } else {
      console.log('=== PROCESS GAME END ===');
      players.sort((a, b) => {return b.score - a.score});
      for (var i = 0; i < players.length; i++) {
        if (players[i].score < 22) {
          $(`#card_${players[i].player_id}`).append(
            '<div class="card-footer"><h4 class="text-success">WINNER</h4></div/>'
          )
          players[i]["winner"] = true;
          break;
        }
      }
      setTimeout(function() { closeGame() }, 5000);
    }

    //showPopup('What would you like to do?', 'action')
  } else {
    if (user_name === 'dealer') {
      showPopup('Click [SETUP] to deal the first round of cards', 'setup');
      $('#setup').click(function(elem) {
        hidePopup();
        // stopTimer();
        for (var i = 0; i < 2; i++) {
          for (var j = 0; j < players.length; j++) {
            var player = players[j];

            if (player.name === "dealer"){
              var dealer = players[j];
            } else {
              addActiveGame(player, card=dealCard(), 'setup');
            }
            if (j === (players.length - 1)) {
              addActiveGame(dealer, card=dealCard(), 'setup');
            }
          }
        }
        location.reload();
        // startTimer();
      });
    } else {
      showPopup('Waiting for the dealer to start...');
      startTimer();
    }
  }
}

function getStats() {
  var temp_stats = {};

  var hand_template = ({ player_hand }) => `${player_hand}`;
  var temp_spectators = [];
  var temp_hands = [];
  var temp_names = [];
  var temp_scores = [];
  var temp_win_name = "";
  var temp_win_email = "";
  var temp_win_score = 0;
  for (var i = 0; i < players.length; i++) {
    var player = players[i];
    var cards = getPlayerCards(player);
    if (player.winner) {
      temp_stats.game_id = player.game_id
      temp_stats.user_id = player.user_id;
      temp_stats.player_id = player.player_id;
      temp_stats.winner = player.name;
      temp_stats.winner_email = player.email;
      temp_stats.winner_hand = cards.map(hand_template).join('+');
      temp_stats.winner_score = player.score;
    }
	  temp_hands.push(cards.map(hand_template).join('+'));
    temp_names.push(player.name);
    temp_scores.push(player.score);
  }
  for (var i = 0; i < spectators.length; i++) {
    temp_spectators.push(spectators[i].name)
  }

  temp_stats.players = temp_names.join(', ');
  temp_stats.player_hands = temp_hands.join(', ');
  temp_stats.player_scores = temp_scores.join(', ');
  temp_stats.spectators = temp_spectators.join(', ');

  return temp_stats;
}

function saveActiveGame() {
  /*
   * POST: https://deckdealer.hopto.org/delete/active_game2
   * PARAMS: (example):
   * {
   *   game_id: 1,
   *   user_id: 2,
   *   player_id: 1,
   *   winner: "dealer",
   *   winner_email: "dealer@udel.edu",
   *   winner_hand: "10S, 10H",
   *   winner_score: 20,
   *   players: "dealer, alice, bob",
   *   player_hands: "10S+10H, 6D+QH+3S, 4H+9D+5S",
   *   player_scores: "20, 19, 18",
   *   spectators: "anna, steve",
   * }
   */
  var url = new URL('/add/score_board2', api_url).toString();
  var stats = getStats();
  $.ajax({url: url, type: 'POST', async: false,
    data: stats,
    success: function(response) {
      console.log(response);
    }
  });

}

function clearActiveGame() {
  /*
   * POST: https://deckdealer.hopto.org/delete/active_game2
   * PARAMS: (example):
   * { filter: `(entry_id > 0)` }
   */
  var url = new URL('/delete/active_game2', api_url).toString();
  $.ajax({url: url, type: 'POST', async: false,
    data: {
      filter: `(entry_id > 0)`,
    },
    success: function(response) {
      console.log(response);
    }
  });
}

function clearPlayers() {
  /*
   * POST: https://deckdealer.hopto.org/delete/players2
   * PARAMS: (example):
   * { filter: `(entry_id > 0)` }
   */
  var url = new URL('/delete/players2', api_url).toString();
  $.ajax({url: url, type: 'POST', async: false,
    data: {
      filter: `(user_id > 0)`,
    },
    success: function(response) {
      console.log(response);
    }
  });
}

function clearSpectators() {
  /*
   * POST: https://deckdealer.hopto.org/delete/spectators2
   * PARAMS: (example):
   * { filter: `(entry_id > 0)` }
   */
  var url = new URL('/delete/spectators2', api_url).toString();
  $.ajax({url: url, type: 'POST', async: false,
    data: {
      filter: `(user_id > 0)`,
    },
    success: function(response) {
      console.log(response);
    }
  });
}


function closeGame() {
  clearInterval(timer);
  if (user_name === 'dealer') {
    showPopup('Click [CLOSE GAME] to add the results to the score_board', 'close');
    $('#close').click(function(elem) {
      hidePopup();
      saveActiveGame();
      clearActiveGame();
      clearPlayers();
      clearSpectators();
    })
  }
}

function startTimer(ms=5000) {
  timer = setInterval(function() { location.reload(); }, ms);
}

function stopTimer() {
  clearInterval(timer);
}

$(document).ready(function() {
  /* set variables */
  html = $('#player-list').html();
  user_id   = getUserID();
  user_name = getUserName();

  players     = getPlayers();
  player_id   = getPlayerID();
  player_name = getPlayerName();
  spectators  = getSpectators();

  /* debug: check local variables */
  console.log('user_id = ' + user_id);
  console.log('=== players ===')
  console.table(players);

  $('#game-play').html('Blackjack: (' + player_name + ')');

  /* generate HTML: every 500 ms */
  //startTimer();
  showActiveGame();

});
