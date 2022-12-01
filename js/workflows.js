var api_url = "https://deckdealer.hopto.org";
var token = getToken(api_url);

function getToken(api_url) {
  var urlParams = new URLSearchParams(window.location.search);
  console.log('=== TOKEN ===');
  console.log(urlParams.get('token'));
  return urlParams.get('token');
}

function sendRequest(path, data) {
  var url = new URL(path, api_url);
  $('#response').removeClass('d-none');

  $.ajax({
    url: url,
    method: 'POST',
    data: data,
    accepts: {table: 'application/x-table'},
    converters: {
      'text table': function(result) { return result; }
    },
    dataType: 'table',
    success: function(data, status, xhr) {
      console.log("Status: " + status);
      $('#response').html(data);
    },
    error: function(xhr, status, error) {
      console.log("ERROR: " + status + " " + error + " " + xhr.status + " " + xhr.statusText);
    }

  }).then(function() {
    $('table').DataTable({
      dom: '<"top">rt<"bottom"flp><"clear">',
    });
  });
}

function sendJSON(path, data) {
  var url = new URL(path, api_url);
  $('#response').removeClass('d-none');
  console.table(data);

  $.ajax({
    url: url,
    method: 'POST',
    data: data,
    success: function(data, status, xhr) {
      console.log("Status: " + status);
      $('#response').html('<div class="col-12 fw-bold lh-lg">Response:</div>')
      $('#response').append('JSON: {\n');
      $.each(data, function(key, value) {
        $('#response').append('  <span class="text-info">"' + key + '"</span>');
        $('#response').append('<span class="text-warning">: </span>');
        $('#response').append('<span class="text-success">"' + value + '"</span>,\n');
      });
      $('#response').append('}\n');
    },
    error: function(xhr, status, error) {
      console.log("ERROR: " + status + " " + error + " " + xhr.status + " " + xhr.statusText);
    }
  });
}

function customSort(a, b) {
  if (a.name.includes('user') && b.name.includes('user')) {
    return 0;
  } else if (a.name.includes('user')) {
    return -1;
  } else if (b.name.includes('user')) {
    return 1;
  } else {
    if (a.name < b.name) {
      return -1;
    } else {
      return 1;
    }
  }
}

function getParams() {
  var endpoint = $('#endpoint').val();
  $('#response').addClass('d-none');

  if ((endpoint === "/get") || (endpoint === "/add") || (endpoint === "/edit") || (endpoint === "/delete")) {
    $('#table-col').removeClass('d-none');

    var table = $('#tables').val();
    if (endpoint == "/get") {
      var path = "/delete/" + table;
    } else {
      var path = endpoint + '/' + table;
    }
    var url = new URL(path, api_url);
    url.searchParams.append('token', token);

    $.get(url, function(data, status) {
      var required = '';
      var params = {};

      $('#params-row').removeClass('d-none');
      if (endpoint === "/add") {
        $('#filter-col').addClass('d-none');
        $('#params-row').html('<div class="col-12 fw-bold lh-lg">Add Parameters (All Required):<div>');
        params = data.required;
        required = ' required';
      }
      if (endpoint === "/get") {
        $('#filter-col').removeClass('d-none')
        $('#params-row').html('<div class="col-12 fw-bold lh-lg">Add Parameters (Optional):<div>');
        params = data.query_params;
      }
      if (endpoint === "/edit") {
        $('#filter-col').removeClass('d-none')
        $('#params-row').html('<div class="col-12 fw-bold lh-lg">Add Parameters (At Least 1 to Edit):<div>');
        params = data.editable;
      }
      if (endpoint === "/delete") {
        $('#filter-col').removeClass('d-none')
        $('#params-row').html('<div class="col-12 fw-bold lh-lg">Add Parameters (At Least 1 to Filter By [or use filter]):<div>');
        params = data.query_params;
      }
      $.each(params, function(index, item) {
        $.each(item, function(key, val) {
          if (key != "filter") {
            var tmp = '<div class="col-2"><div class="input-group"><div class="input-group-text">' + key + ' =</div><input type="text" class="form-control" name="' + key + '" onchange="updateAPI();"' + required + '></div></div>';
            $('#params-row').append(tmp);
          }
        });
        if (index === (params.length - 1)) {
          $('input').change(updateAPI());
        }
      });
    });
  }
  if ((endpoint === '/login') || (endpoint === '/register') || (endpoint === '/uploadImageUrl')) {
    var url = new URL(endpoint, api_url);
    url.searchParams.append('token', token);
    $.get(url, function(data, status) {
      var params = data.required;
      $('#table-col').addClass('d-none');
      $('#filter-col').addClass('d-none');
      $('#params-row').removeClass('d-none');
      $('#params-row').html('<div class="col-12 fw-bold lh-lg">Add Parameters (All Required):<div>');
      $.each(params, function(index, item) {
        $.each(item, function(key, val) {
          var tmp = '<div class="col-2"><div class="input-group"><div class="input-group-text">' + key + ' =</div><input type="text" class="form-control" name="' + key + '" onchange="updateAPI();" required></div></div>';
          $('#params-row').append(tmp);
        });
        if (index === (params.length - 1)) {
          $('input').change(updateAPI());
        }
      });
    });
  }
  if ((endpoint === '/logout') || (endpoint === '/status')) {
    $('#table-col').addClass('d-none');
    $('#filter-col').addClass('d-none');
    $('#params-row').addClass('d-none');
    updateAPI();
  }
  if (endpoint === '/deleteTable') {
    $('#table-col').removeClass('d-none');
    $('#filter-col').addClass('d-none');
    $('#params-row').addClass('d-none');
    updateAPI();
  }
  if (endpoint === '/createTable') {
    $('#table-col').addClass('d-none');
    $('#filter-col').addClass('d-none');
    $('#params-row').removeClass('d-none');
    $('#params-row').html('<div class="col-12 fw-bold lh-lg">Add Parameters ({ref}_id and {ref_time} are Required):<div>');
    var placeholder = '/user_profiles/entry_id/INTEGER/user_id/INTEGER/name/TEXT/email/TEXT/profile_pic/TEXT/entry_time/DATETIME'
    $('#params-row').append('<div class="col-12"><div class="input-group"><div class="input-group-text">{table_name}/column/type =</div><input type="text" class="form-control" name="col-type" onchange="updateAPI();" placeholder="'+placeholder+'" required></div></div>');
    updateAPI();

  }
}

function getTables(api_url, token) {
  var url = new URL('/get', api_url);
  url.searchParams.append('token', token);

  $.get(url, function(data, status) {
    data.tables.sort(customSort);
    $('#tables').html('');
    $.each(data.tables, function(index, tbl) {
      $('#tables').append('<option value="' + tbl.name + '">' + tbl.name+ '</option>');
      if (index === (data.tables.length - 1)) {
        console.log('TABLES = ' + $('#tables').val())
        getParams();
        $('#tables').change(function() {
          getParams();
          updateAPI()
        });
      }
    });
  });
}

function updateAPI() {
  var endpoint = $('#endpoint').val();
  if (!$('#table-col').hasClass('d-none')) {
    var path = endpoint + '/' + $('#tables').val();
  } else {
    var path = endpoint;
  }
  var url = new URL(path, api_url);

  var data = {}
  if (!$('#params-row').hasClass('d-none')) {
    $.each($('#params-row').find('input'), function(index, item) {
      if (endpoint === '/createTable') {
        path = path + item.value;
        console.log(path);
        url = new URL( path, api_url);
        console.log(url);
      } else if (item.value) {
        data[item.name] = item.value;
      }
    });
  }
  if (!$('#filter-col').hasClass('d-none')) {
    $.each($('#filter-col').find('input'), function(index, item) {
      if (item.value) {
        data[item.name] = item.value;
      }
    });
  }
  data['token'] = token;
  $('#request').html('URL: <span class="text-primary">' + url + '</span>\n')
  $('#request').append('JSON: {\n')
  $.each(data, function(key, value) {
    $('#request').append('  <span class="text-info">"' + key + '"</span>');
    $('#request').append('<span class="text-warning">: </span>');
    $('#request').append('<span class="text-success">"' + value + '"</span>,\n');
  })
  $('#request').append('}\n')

  return {path, data};
}

function errorMessage(message) {
  $('#message').html("Error Processing Params:");
  $('#message-body').html(message);
  $('#popup').modal("show");
  return false
}

function checkParams() {
  var endpoint = $('#endpoint').val();
  var params = $('#params-row').find('input');
  var count = 0;
  for (var i=0; i<params.length; i++) {
    if ((params[i].hasAttribute('required') && (params[i].value)) || (params[i].value)) {
      count++;
    }
  }
  if (((endpoint === '/add') || (endpoint === '/login') || (endpoint === '/register') || (endpoint === '/uploadImageUrl')) && (count !== params.length))  {
    return errorMessage('All Parameters Must Have a Value');
  }
  if (((endpoint === '/edit') || (endpoint === '/delete')) && (count === 0)) {
    return errorMessage("At Least 1 Parameter Must Be Set");
  }
  return true;
}

$(document).ready(function() {
  // -- on page load, /get is selected
  getTables(api_url, token);

  $('#submit').click(function(e) {
    if (checkParams()) {
      var endpoint = $('#endpoint').val();
      var {path, data} = updateAPI();
      if ((endpoint === "/get") || (endpoint === "/add") || (endpoint === "/edit") || (endpoint === "/delete")) {
        return sendRequest(path, data);
      } else {
        if ((endpoint === '/deleteTable') || (endpoint === '/createTable')) {
          sendJSON(path, data);
          return getTables(api_url, token)
        } else {
          return sendJSON(path, data);
        }
      }
    }
  });

  $(document).keypress(function(e) {
    if (e.which == 13) {
      $('#submit').click();
    }
  })
});
