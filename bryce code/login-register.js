/*Check*/
  $(document).ready(function() {
    var api_url = "https://deckdealer.hopto.org"
    var user_id = "";
  
    function showPopUp(message, data) {
      if (message.includes('user login success')) {
        $('#popup-content').append(
          '<div class="modal-footer">' +
            '<div class="container">' +
              '<div class="row justify-content-center">' +
                '<div class="col">' +
                  '<a class="btn btn-primary form-control btn-block" href="spectator-register.html">Watch Game</a>' +
                '</div>' +
                '<div class="col">' +
                  '<a class="btn btn-primary form-control btn-block" href="game.html">Play Game</a>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>'
        )
      }
      $('#message').html(message);
      $('#message-body').html(message_body);
      $('#popup').modal("show");
    }
  
    $("#login").submit(function(e) {
      e.preventDefault();
      var url = new URL("/login", api_url).toString()
      var message = "";
      $.post(url, {
        username: $('#username-login').val(),
        password: $('#password-login').val()
      }, function(data, status) {
        console.log("Status: " + status);
        if (data.message === undefined) {
          message = "No [message] in the Response...";
        } else {
          message = data.message;
          delete data.message;
        }
        message_body = data;
        showPopUp(message, data);
      });
    });
  
    $("#register").submit(function(e) {
      e.preventDefault();
      var url = new URL("/login", api_url).toString()
      $.post(url, {
        username:  $('#username-register').val(),
        password:  $('#password-register').val(),
        password2: $('#password2-register').val(),
      }, function(data, status) {
        console.log("Status: " + status);
        if (data.message === undefined) {
          console.table(data);
          message = "No [message] in the Response...";
        } else {
          message = data.message;
          delete data.message;
        }
        message_body = data;
        $('#message').html(message);
        $('#message-body').html(message_body);
        $('#popup').modal("show");
      });
    });
  });
  