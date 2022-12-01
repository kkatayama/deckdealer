$(document).ready(function() {
    var api_url = "https://deckdealer.hopto.org"
    var user_id = "";
    var token   = "";
  
    $("#login").submit(function(e) {
      e.preventDefault();
      var url = new URL("/login", api_url).toString()
      var message = "";
      $.post(url, {
        username: $('#username_login').val(),
        password: $('#password_login').val()
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
        $('#popup').on('hide.bs.modal', function() {
          if (message.includes('user login success')) {
            console.log("LOGIN SUCCESS");
            console.table(data);
            var main = "workflows.html?token=" + data.token;
            window.location.href = main;
          } else {
            console.log("LOGIN FAILED");
            console.table(data);
          }
  
          console.log(message)
        });
      });
    });
  
    $("#register").submit(function(e) {
      e.preventDefault();
      var url = new URL("/login", api_url).toString()
      $.post(url, {
        username:  $('#username_register').val(),
        password:  $('#password_register').val(),
        password2: $('#password2_register').val(),
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
  