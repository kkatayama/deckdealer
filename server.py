# -- bottle framework & plugins
from bottle import hook, route, run, request, response, template, static_file, HTTPError, json_dumps
from bottle_sqlite import SQLitePlugin, sqlite3
from bottle_cors_plugin import cors_plugin
import bottle
import requests
import mimetypes

# -- /utils/db_functions.py
from utils.db_functions import (
    insertRow, fetchRow, fetchRows, updateRow, deleteRow,
    addTable, deleteTable, getTable, getTables, getColumns,
    securePassword, checkPassword, genToken, require_uid, User,
    clean, extract, mapUrlPaths, uploadImage,
    getLogger, log_to_logger, logger, checkUserAgent,
    parseURI, parseUrlPaths, parseFilters, parseColumnValues,
    parseParams, ErrorsRestPlugin, secret_key, get_py_path, py_path,
)

# -- /docs/usage.py
from docs.usage import (
    usage_add, usage_get, usage_edit, usage_delete,
    usage_create_table, usage_delete_table,
    usage_login, usage_logout, usage_register,
    usage_uploadImageUrl
)

# -- pretty parsing
import pandas as pd
from pathlib import Path
from rich import print, inspect
import json
import sys
import os
import re


# -- app setup
app = bottle.app()
db_file = Path.cwd().joinpath('db', 'backend.db')
plugin = SQLitePlugin(dbfile=db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
app.install(plugin)
app.install(log_to_logger)
app.install(ErrorsRestPlugin())
app.install(cors_plugin([
    'https://deckdealer.hopto.org',
    'http://localhost:3000', 'http:/127.0.0.1:3000', 'http://0.0.0.0:3000',
    'http://localhost:8080', 'http:/127.0.0.1:8080', 'http://0.0.0.0:8080',
    'http://localhost:8888', 'http:/127.0.0.1:8888', 'http://0.0.0.0:8888',
    'null']))

print(f'py_path: {py_path}')
print(f'get_py_path: {get_py_path()}')

# -- helper function to return Pandas generated HTML Table when expected in request...
def genTable(records, caption, count=0):
    table_id = f'response{count}'
    styles = [dict(selector="caption", props=[("text-align", "center"), ("font-size", "150%"), ("color", 'black')])]
    df = pd.DataFrame.from_records(records)
    s = df.style.set_caption(caption).set_table_styles(styles)
    table = s.to_html()
    html = re.sub(r'( id="(T_[_a-z0-9]+)"| class="([_a-z0-9 ]+)" |<style.*</style>\n)', '', table, flags=re.DOTALL)
    html = re.sub(r'([_0-9a-zA-Z]+\.(png|jpg|jpeg|svg|bmp|gif|tiff))', r'<img src="https://deckdealer.hopto.org/\1" height="100"></img>', html)
    html = html.replace('<th>&nbsp;</th>', '<th>index</th>')
    html = html.replace('<table>', f'<table id="{table_id}" class="table caption-top table-striped table-hover" style="width:100%">')

    # html = re.sub(r'table id="(T_[a-z0-9]+)"', f'table id="{table_id}"', table)
    # html = re.sub(r'( id="(T_[_a-z0-9]+)"| class="([_a-z0-9 ]+)" )', '', html)
    # html = re.sub(r'<style.*</style>\n', '', html, flags=re.DOTALL)
    return html

def checkType(res):
    if 'x-table' in request.headers.get('Accept'):
        response.content_type = "application/x-table"
        if not isinstance(res, dict):
            return clean(res)

        caption = "no message?"
        if res.get('message'):
            caption = 'TABLE: message: ' + res.pop('message')
        elif res.get('Error'):
            caption = 'Error: ' + res.pop('Error')
        elif res.get('Python_Error'):
            caption = 'Python_Error: ' + res.pop('Python_Error')
        elif res.get("MimeType_Error"):
            caption = "MimeType_Error: " + res.pop("MimeType_Error")
        elif [key for key in res.keys() if 'SQLite.' in key]:
            key = [key for key in res.keys() if 'SQLite.' in key][0]
            caption = key + ': ' + res.pop(key)
        print(f'caption = {caption}')

        html = ""
        if res.get('data') and len(res.keys()) == 1:
            print('parsing: data')
            res = res.pop('data')
            records = [res] if isinstance(res, dict) else res
            html = genTable(records, caption)
        elif res.get('tables') and len(res.keys()) == 1:
            print('parsing: tables')
            res = res.pop('tables')
            records = [res] if isinstance(res, dict) else res
            html = ""
            for i, record in enumerate(records):
                html += genTable(record, caption=f'{caption}: {record["name"]}', count=i)

        return clean(template(html))
    return clean(res)

# -- hook to strip trailing slash
@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
    parseParams(secret_key)

# -- hook to allow cross origin
@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Credentials'] = 'true'

# -- index - response: running
@route("/", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def index():
    dirname = sys.path[0]
    return static_file('index.html', root=f'{dirname}')

# -- usage - response: available commands
@route("/usage", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def usage():
    res = {
        "message": "API_Endpoints",
        "User_Functions": {
            "/login": usage_login, "/logout": usage_logout, "/register": usage_register,
        },
        "Admin_Functions": {
            "/createTable": usage_create_table, "/deleteTable": usage_delete_table,
        },
        "Core_Functions": {
            "/add": usage_add, "/get": usage_get, "/edit": usage_edit, "/delete": usage_delete,
        },
        "Extra_Functions": {
            "/uploadImageUrl": usage_uploadImageUrl,
        }
    }
    return checkType(res)

###############################################################################
#                      User's Table: Additional Functions                     #
###############################################################################
@route("/invalidSession", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def invalidSession():
    res = {
        "Unauthorized": "Please log in to use this service!",
        "Note": "Attach your session cookie or token along with your request."
    }
    return checkType({"message": res})

@route("/status", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/status/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def getStatus(db, url_paths=""):
    user = User()
    res = {"message": "Authorized: user is logged in with an active session cookie",
        "user_id": user.user_id, "token": user.token, }
    return checkType(res)

@route("/register", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/register/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def register(db, url_paths=""):
    # -- usage info
    if url_paths == 'usage':
        return usage_register

    # -- parse "params" and "filters" from HTTP request
    table = getTable(db, table_name="users")
    required_columns = getColumns(db, table, required=True)
    params, filters = parseUrlPaths(url_paths, request.params, required_columns)
    params.update(dict(request.params))
    print(f"request.params = {dict(request.params)}\nparams = {params}\nfilters = '{filters}'")

    # -- minimum parameters needed to register a new account
    try:
        username = params["username"]
        plaintext = params["password"]
        password2 = params["password2"]
    except KeyError:
        # res = {"message": "missing parameter", "required params": ["username", "password", "password2"]}
        required_columns.update({'password2': 'TEXT'})
        res = {"message": "missing parameter", "required": [required_columns], "submitted": [params]}
        return checkType(res)

    if plaintext != password2:
        res = {"message": "passwords do not match", "password1": plaintext, "password2": password2}
        return checkType(res)
    params.update({"password": securePassword(params.pop("password"))})

    # -- check if user exists
    if fetchRow(db, table=table, where="username=?", values=params["username"]):
        res = {"message": "user exists", "username": params["username"]}
        return checkType(res)

    # -- if user doesn't exist, create user
    edit_items = {k: params[k] for k in required_columns if params.get(k)}
    columns, col_values = list(edit_items.keys()), list(edit_items.values())
    user_id = insertRow(db, table=table, columns=columns, col_values=col_values)
    res = {"message": "new user created", "user_id": user_id, "username": username}
    return checkType(res)

@route("/login", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/login/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def login(db, url_paths=""):
    # -- usage info
    if url_paths == 'usage':
        return usage_login

    # -- parse "params" and "filters" from HTTP request
    table = getTable(db, table_name="users")
    required_columns = getColumns(db, table, required=True)
    params, filters = parseUrlPaths(url_paths, request.params, required_columns)
    print(f"params = {params}\nfilters = '{filters}'")

    # -- check for required parameters
    if any(k not in params.keys() for k in required_columns):
        res = {"message": "missing parameters", "required": [required_columns], "submitted": [params]}
        return checkType(res)

    # -- check if user exists
    row = fetchRow(db, table="users", where="username=?", values=params["username"])
    if not row:
        res = {"message": "user does not exist", "username": params["username"]}
        return checkType(res)

    # -- check user submitted password against the one retrieved from the database
    if not checkPassword(params["password"], row["password"]):
        res = {"message": "incorrect password", "password": params["password"]}
        return checkType(res)

    # -- send response message
    user = User()
    user.login(str(row["user_id"]))
    res = {"message": "user login success", "user_id": row["user_id"], "username": row["username"]}
    res.update({"token": genToken("user_id", str(row["user_id"]), secret_key)})
    return checkType(res)

@route("/logout", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def logout(db):
    user_id = request.get_cookie("user_id", secret=secret_key)
    res = {"message": "user logged out", "user_id": user_id}
    response.delete_cookie("user_id")
    return checkType(res)

@route("/uploadImageUrl", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/uploadImageUrl/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def uploadImageUrl(url_paths=""):
    # -- usage info
    if url_paths == 'usage':
        return usage_uploadImageUrl

    # -- parse "params" and "filters" from HTTP request
    required_columns = {"url": "TEXT"}
    p = map(str, url_paths.split('/', maxsplit=1))
    params = dict(request.params)
    params.update(dict(zip(p, p)))

    # -- check for required parameters
    if any(k not in params.keys() for k in required_columns):
        res = {"message": "missing parameters", "required": [required_columns], "submitted": [params]}
        return checkType(res)

    # -- fetch raw image data and save image
    res = uploadImage(url=params.get("url"))
    return checkType(res)

###############################################################################
#                          Database Admin Functions                           #
###############################################################################
@route("/createTable", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/createTable/<table_name>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/createTable/<table_name>/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def createTable(db, table_name="", url_paths=""):
    # -- usage info
    if table_name == 'usage':
        return usage_create_table

    required_columns = {"user_id": "INTEGER", "{ref}_id": "INTEGER", "{ref}_time": "DATETIME",
                        "column_name": "column_type",
                        "available_types": ["INTEGER", "DOUBLE", "TEXT", "DATETIME"]}
    if (not table_name):
        return checkType({"message": "active tables in the database", "tables": getTables(db)})
    if ((not url_paths) and (not request.params)):
        res = {"message": "missing paramaters", "required": [required_columns],
               "available_types": ["INTEGER", "DOUBLE", "TEXT", "DATETIME"],
               "Exception": "\"{ref}_id\" not required when creating \"users\" table", "submitted": []}
        return checkType(res)

    # -- parse "params" and "url_paths" from HTTP request
    params, columns = mapUrlPaths(url_paths, request.params, table_name)

    # if not checkCreateTable(params, columns):
    #     res = {"message": "missing paramaters", "required": [required_columns],
    #            "missing": [missing_params], "submitted": [params]}
    #     return checkType(res)

    # -- CREATE TABLE <table>
    res = addTable(db, table=table_name, columns=columns)
    res.update({"table": table_name})
    return checkType(res)

@route("/deleteTable", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/deleteTable/<table_name>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def dropTable(db, table_name=""):
    # -- usage info
    if table_name == 'usage':
        return usage_delete_table

    tables = getTables(db)
    table = getTable(db, tables, table_name)
    if not table:
        return checkType({"message": "active tables in the database", "tables": tables})

    # -- DROP TABLE <table>
    res = deleteTable(db, table=table_name)
    res.update({"table": table_name})
    return checkType(res)

###############################################################################
#                   Core Function /add - Add Data to a Table                  #
###############################################################################
@route("/add", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/add/<table_name>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/add/<table_name>/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def add(db, table_name="", url_paths=""):
    # -- usage info
    if table_name == 'usage':
        return usage_add

    # -- if no table is supplied or the table does not exist, return all active tables
    tables = getTables(db)
    table = getTable(db, tables, table_name)
    if not table:
        return checkType({"message": "active tables in the database", "tables": tables})

    # -- parse "params" and "filters" from HTTP request
    required_columns = getColumns(db, table, required=True)
    params, filters = parseUrlPaths(url_paths, request.params, required_columns)

    # -- check for required parameters
    missing_keys = (params.keys() ^ required_columns.keys())
    missing_params = {k: table["columns"][k] for k in required_columns if k in missing_keys}
    if missing_params:
        res = {"message": "missing paramaters", "required": [required_columns],
               "missing": [missing_params], "submitted": [params]}
        return checkType(res)

    # -- the users table requires additional formatting and checking
    if table_name == "users":
        params.update({"password": securePassword(params["password"])})
        if fetchRow(db, table=table, where="username=?", values=params["username"]):
            res = {"message": "user exists", "username": params["username"]}
            return checkType(res)

    # -- define "columns" to edit and "values" to insert
    edit_items = {k: params[k] for k in required_columns if params.get(k)}
    columns, col_values = list(edit_items.keys()), list(edit_items.values())

    # -- query database -- INSERT INTO oximeter (user_id,heart_rate,...) VALUES (?, ?, ...);
    col_id = insertRow(db, table=table, columns=columns, col_values=col_values)
    if isinstance(col_id, dict):
        if col_id.get('Error'):
            return checkType(col_id)

    # -- send response message
    col_ref = getColumns(db, table, ref=True)  # -- get (.*_id) name for table
    res = {"message": f"data added to <{table_name}>", col_ref: col_id}
    for r in re.findall(r"(\w*_id)", " ".join(required_columns)):
        res[r] = params.get(r)

    return checkType(res)

###############################################################################
#                 Core Function /get - Fetch Data From a Table                #
###############################################################################
@route("/get", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/get/<table_name>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/get/<table_name>/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def get(db, table_name="", url_paths=""):
    # -- usage info
    if table_name == 'usage':
        return usage_get

    tables = getTables(db)
    table = getTable(db, tables, table_name)
    if not table:
        return checkType({"message": "active tables in the database", "tables": tables})

    # -- parse "params" and "filters" from HTTP request
    params, filters = parseUrlPaths(url_paths, request.params, table["columns"])

    # -- build "conditions" string and "values" array for "fetchRows()"
    conditions = " AND ".join([f"{param}=?" for param in params.keys()])
    values = list(params.values())
    if filters:
        conditions, values = parseFilters(filters, conditions, values)

    # -- query database -- SELECT * FROM users WHERE (user_id=?);
    rows = fetchRows(db, table=table, where=conditions, values=values)
    if isinstance(rows, dict):
        if rows.get('Error'):
            return checkType(rows)
        message = f"1 {table_name.rstrip('s')} entry found"
    elif isinstance(rows, list):
        message = f"found {len(rows)} {table_name.rstrip('s')} entries"
    else:
        message = f"0 {table_name.rstrip('s')} entries found using submitted parameters"
        rows = {"submitted": [params] + [{"filter": filters}]}

    # -- send response message
    res = {"message": message, "data": rows}
    return checkType(res)

###############################################################################
#                  Core Function /edit - Edit Data in a Table                 #
###############################################################################
@route("/edit", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/edit/<table_name>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/edit/<table_name>/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def edit(db, table_name="", url_paths=""):
    # -- usage info
    if table_name == 'usage':
        return usage_edit

    # # -- only logged in users can access this endpoint
    # user_id = request.get_cookie("user_id", secret=secret_key)
    # if not user_id:
    #     return {'message': 'invalid token'}
    # if request.params.get('token'):
    #     del request.params["token"]

    tables = getTables(db)
    table = getTable(db, tables, table_name)
    if not table:
        return checkType({"message": "active tables in the database", "tables": tables})

    # -- parse "params" and "filters" from HTTP request
    editable_columns = getColumns(db, table, editable=True)
    non_edit_columns = getColumns(db, table, non_editable=True)
    params, filters = parseUrlPaths(url_paths, request.params, table["columns"])
    print(f"params = {params}\nfilters = '{filters}'")

    # -- the users table requires additional formatting and checking
    if (table_name == "users") and params.get("password"):
        params.update({"password": securePassword(params["password"])})

    # -- at least 1 edit parameter required
    if not (editable_columns.keys() & params.keys()):
        submitted = {**{"filter": filters}, **params} if filters else params
        res = {"message": "missing a parameter to edit", "editable": [editable_columns],
               "submitted": [submitted]}
        return checkType(res)

    # -- at least 1 query parameter required
    # TODO: add try except for (submitted)
    submitted = {**{"filter": filters}, **params} if filters else params
    query_params = {**non_edit_columns, **{"filter": filters}}
    if not (submitted.keys() & query_params.keys()):
        res = {"message": "missing a query parameter", "query_params": [query_params], "submitted": [submitted]}
        return checkType(res)

    # -- define "columns" to edit and "values" to insert (parsed from params in HTTP request)
    edit_items = {k: params[k] for k in editable_columns if params.get(k)}
    columns, col_values = list(edit_items.keys()), list(edit_items.values())

    # -- build "conditions" string and "values" string/array for "updateRow()"
    conditions = " AND ".join([f"{param}=?" for param in non_edit_columns if params.get(param)])
    values = [params[param] for param in non_edit_columns if params.get(param)]
    if filters:
        conditions, values = parseFilters(filters, conditions, values)

    # -- query database -- UPDATE users SET username=? WHERE (user_id=?);
    args = {
        "table": table, "columns": columns, "col_values": col_values,
        "where": conditions, "values": values
    }
    num_edits = updateRow(db, **args)
    if isinstance(num_edits, dict):
        if num_edits.get('Error'):
            return checkType(num_edits)
    elif num_edits:
        if num_edits == 1:
            message = f"edited 1 {table_name.rstrip('s')} entry"
        else:
            message = f"edited {num_edits} {table_name.rstrip('s')} entries"
    else:
        message = f"0 {table_name.rstrip('s')} entries found matching your parameters"

    # -- send response message
    res = {"message": message, "submitted": [submitted]}
    return checkType(res)

###############################################################################
#             Core Function /delete - Delete Data from a Table                #
###############################################################################
@route("/delete", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/delete/<table_name>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@route("/delete/<table_name>/<url_paths:path>", method=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@require_uid
def delete(db, table_name="", url_paths=""):
    # -- usage info
    if table_name == 'usage':
        return usage_delete

    tables = getTables(db)
    table = getTable(db, tables, table_name)
    if not table:
        return checkType({"message": "active tables in the database", "tables": tables})

    # -- parse "params" and "filters" from HTTP request
    params, filters = parseUrlPaths(url_paths, request.params, table["columns"])
    print(f"params = {params}\nfilters = '{filters}'")

    # -- to prevent accidental deletion of everything, at least 1 parameter is required
    submitted = {**{"filter": filters}, **params} if filters else params
    query_params = {**table["columns"], **{"filter": filters}}
    if not (submitted.keys() & query_params.keys()):
        res = {"message": "missing a query param(s)", "query_params": [query_params], "submitted": [submitted]}
        return checkType(res)

    # -- build "conditions" string and "values" string/array for "updateRow()"
    conditions = " AND ".join([f"{param}=?" for param in table["columns"] if params.get(param)])
    values = [params[param] for param in table["columns"] if params.get(param)]
    if filters:
        conditions, values = parseFilters(filters, conditions, values)

    # -- query database -- DELETE FROM users WHERE (user_id=?);
    num_deletes = deleteRow(db, table=table, where=conditions, values=values)
    if isinstance(num_deletes, dict):
        if num_deletes.get('Error'):
            return checkType(num_deletes)
        print('=== num_deletes ===')
        print(num_deletes)
    elif num_deletes:
        if num_deletes == 1:
            message = f"1 {table_name.rstrip('s')} entry deleted"
        else:
            message = f"{num_deletes} {table_name.rstrip('s')} entries deleted"
    else:
        message = f"0 {table_name.rstrip('s')} entries found matching your parameters"

    # -- send response message
    res = {"message": message, "submitted": [submitted]}
    return checkType(res)

###############################################################################
#                                 Static Files                                #
###############################################################################
@route('/<filename:re:.*\.html>')
@route('/html/<filename:re:.*\.html>')
@route('/static/html/<filename:re:.*\.html>')
def send_html(filename):
    kind = 'html'
    dirname = sys.path[0]
    if not Path(dirname, filename).exists():
        if Path(dirname, kind, filename).exists():
            dirname = str(Path(dirname, kind))
        if Path(dirname, 'static', kind, filename).exists():
            dirname = str(Path(dirname, 'static', kind))
    response.set_header("Cache-Control", "no-store")
    return static_file(filename, root=f'{dirname}')

@route('/<filename:re:.*\.js>')
@route('/js/<filename:re:.*\.js>')
@route('/static/js/<filename:re:.*\.js>')
def send_js(filename):
    kind = 'js'
    dirname = sys.path[0]
    if not Path(dirname, filename).exists():
        if Path(dirname, kind, filename).exists():
            dirname = str(Path(dirname, kind))
        if Path(dirname, 'static', kind, filename).exists():
            dirname = str(Path(dirname, 'static', kind))
    response.set_header("Cache-Control", "no-store")
    return static_file(filename, root=f'{dirname}')

@route('/<filename:re:.*\.css>')
@route('/css/<filename:re:.*\.css>')
@route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    kind = 'css'
    dirname = sys.path[0]
    if not Path(dirname, filename).exists():
        if Path(dirname, kind, filename).exists():
            dirname = str(Path(dirname, kind))
        if Path(dirname, 'static', kind, filename).exists():
            dirname = str(Path(dirname, 'static', kind))
    response.set_header("Cache-Control", "no-store")
    return static_file(filename, root=f'{dirname}')

@route(f"/<filename:re:.*\.({'|'.join(m.strip('.') for m in mimetypes.types_map)})>")
@route(f"/img/<filename:re:.*\.({'|'.join(m.strip('.') for m in mimetypes.types_map)})>")
@route(f"/static/img/<filename:re:.*\.({'|'.join(m.strip('.') for m in mimetypes.types_map)})>")
def send_img(filename):
    kind = 'img'
    dirname = sys.path[0]
    if not Path(dirname, filename).exists():
        if Path(dirname, kind, filename).exists():
            dirname = str(Path(dirname, kind))
        if Path(dirname, 'static', kind, filename).exists():
            dirname = str(Path(dirname, 'static', kind))
    return static_file(filename, root=f'{dirname}')


###############################################################################
#                                Run Web Server                               #
###############################################################################
mimetypes.init()
port = int(os.environ.get("PORT", 8888))
run(app, host="0.0.0.0", port=port, reloader=True, debug=False)
