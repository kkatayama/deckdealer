###############################################################################
#                           Overview of DB Functions                          #
###############################################################################
"""
These functions connect to the SQLite Database and execute transactions.
All functions use "parametrized queries" to prevent SQL injection attacks.
All functions support a full SQL [query] or a python [dict]

  * insertRow()  - Insert data into the database
  * fetchRow()   - Fetch a single row from a table in the database
  * fetchRows()  - Fetch multiple rows from a table in the database
  * updateRow()  - Update data in the database
  * deleteRow()  - Delete row(s) from the database
"""

###############################################################################
#                         Overview of Helper Functions                        #
###############################################################################
"""
These functions
# -- securePassword()   - create a password (sha256 hash, salt, and iterate)
# -- checkPassword()    - check if password matches
# -- clean()            - sanitize data for json delivery
"""

from bottle import request, response, FormsDict, WSGIHeaderDict, json_dumps, JSONPlugin, template, cookie_decode, cookie_encode, HTTPError
from base64 import b64decode, b64encode
from datetime import datetime
from bs4 import BeautifulSoup

from logging.handlers import TimedRotatingFileHandler
from functools import wraps
from rich import print, inspect

# import subprocess
import traceback
import logging
import hashlib
import codecs
import sqlite3
# import time

from requests.exceptions import RequestException
from utils.paths import get_py_path
from pathlib import Path
import mimetypes
import requests
import json
import sys
import os
import re


response.debug = []

###############################################################################
#                              CREATE OPERATIONS                              #
###############################################################################
def insertRow(db, query="", **kwargs):
    """
    Insert data into the database

    ARGS:
        Required - db (object)          - the database connection object
        Optional - query (str)          - a complete SQL query

        Required - table (str)          - the table to insert data into
        Required - columns (list)       - the columns to edit
        Required - col_values (list)    - the values for the columns
    RETURNS:
        lastrowid (int) OR False - the last ID for the transaction

    EXAMPLE: with [query]
        query = "INSERT INTO users (username,password,create_time) VALUES ("user_01", "user_01", "2022-03-15")"
        user_id = insertRow(db, query=query)

    EXAMPLE: with [query] and [col_values]
        user_id = insertRow(db, query=INSERT INTO users (username,password,create_time) VALUES (?, ?, ?),
                            col_values=["user_01", "user_01", "2022-03-15"])

    EXAMPLE: with [params] directly
        user_id = insertRow(db, table="users", columns=["username", "password", "create_time"],
                            col_values=["user_01", "user_01", "2022-03-15"])

    EXAMPLE: with [params] as (dict)
        params = {
            "table": "users",
            "columns": ["username", "password", "create_time"],
            "col_values": [username, password, create_time],
        }
        user_id = insertRow(db, **params)
    """
    if query:
        table = ""
        columns = []
        col_values = kwargs.get("col_values")
    else:
        # table      = kwargs["table"]
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        columns = kwargs["columns"]
        col_values = kwargs["col_values"]
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({', '.join(['?']*len(columns))});"
    log_sqlite(query), log_sqlite(col_values) if col_values else log_sqlite(query)

    try:
        cur = db.execute(query, col_values) if col_values else db.execute(query)
    except sqlite3.Error as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_msgs = traceback.format_exception(exc_type, exc_value, exc_tb)
        if isinstance(tb_msgs, list):
            tb_msgs = ''.join(tb_msgs).splitlines()
        err = {
            f'SQLite.{e.__class__.__name__}': f'{" ".join(e.args)}',
            'Debug Info': {
                "query": query,
                "kwargs": kwargs,
                "parsed": {"table": table, "columns": columns, "col_values": col_values}
            },
            'SQLite Traceback': tb_msgs
        }
        # logger.error(err)
        return err

    return cur.lastrowid

###############################################################################
#                               READ OPERATIONS                               #
###############################################################################
def fetchRow(db, query="", **kwargs):
    """
    Fetch a single row from a table in the database

    ARGS:
        Required - db (object)          - the database connection object
        Optional - query (str)          - a complete SQL query

        Required - table (str)          - the table to fetch data from
        Optional - columns (list)       - columns to filter by
        Optional - where (str)          - conditional "WHERE" statement
        Optional - values (str|list)    - the value(s) for the "WHERE" statement
    RETURNS:
        row (dict) OR False - the row data as a (dict) object

    EXAMPLE: with [query]
        row = fetchRow(db, query="SELECT * FROM users;")

    EXAMPLE: with [query] and [values]
        row = fetchRow(db, query="SELECT * FROM users WHERE (user_id=?);", values=["5"])

    EXAMPLE: with [params] directly
        row = fetchRow(db, table="users", where="user_id=?", values="5")

    EXAMPLE: with [params] as (dict)
        user_id = "5"
        params = {
            "table": "users",
            "where": "user_id=?",
            "values": user_id
        }
        row = fetchRow(db, **params)
    """
    if query:
        table = ""
        columns = []
        condition = ""
        values = [kwargs.get("values")] if isinstance(kwargs.get("values"), str) else kwargs.get("values")
    else:
        # table     = kwargs.get("table")
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        columns = "*" if not kwargs.get("columns") else ",".join(kwargs["columns"])
        condition = "1" if not kwargs.get("where") else f'{kwargs["where"]}'
        values = [kwargs.get("values")] if isinstance(kwargs.get("values"), str) else kwargs.get("values")
        query = f"SELECT {columns} FROM {table} WHERE {condition};"
    log_sqlite(query), log_sqlite(values) if values else log_sqlite(query)

    try:
        row = db.execute(query, values).fetchone() if values else db.execute(query).fetchone()
    except sqlite3.Error as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_msgs = traceback.format_exception(exc_type, exc_value, exc_tb)
        if isinstance(tb_msgs, list):
            tb_msgs = ''.join(tb_msgs).splitlines()
        err = {
            f'SQLite.{e.__class__.__name__}': f'{" ".join(e.args)}',
            'Debug Info': {
                "query": query,
                "kwargs": kwargs,
                "parsed": {"table": table, "columns": columns, "condition": condition, "values": values}
            },
            'SQLite Traceback': tb_msgs
        }
        # logger.error(err)
        return err

    if row:
        return dict(row)
    return False

def fetchRows(db, query="", **kwargs):
    """
    Fetch multiple rows from a table in the database

    ARGS:
        Required - db (object)          - the database connection object
        Optional - query (str)          - a complete SQL query

        Required - table (str)          - the table to fetch data from
        Optional - columns (list)       - columns to filter by
        Optional - where (str)          - conditional "WHERE" statement
        Optional - values (str|list)    - the value(s) for the "WHERE" statement

        Optional - force (bool)         - force return type list
    RETURNS:
        rows (list[(dict)]) OR False - the rows of data as a (list) of (dict) objects

    EXAMPLE: with [query]
        rows = fetchRows(db, query="SELECT * FROM users;")

    EXAMPLE: with [query] and [values]
        rows = fetchRows(db, query="SELECT * FROM users WHERE (user_id=?);", values=["5"])

    EXAMPLE: with [params] directly
        rows = fetchRows(db, table="users", where="user_id=?", values="5")

    EXAMPLE: with [params] as (dict)
        user_id = "5"
        params = {
            "table": "users",
            "where": "user_id=?",
            "values": user_id
        }
        rows = fetchRows(db, **params)
    """
    if query:
        table = ""
        columns = []
        condition = ""
        values = [kwargs.get("values")] if isinstance(kwargs.get("values"), str) else kwargs.get("values")
    else:
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        columns = "*" if not kwargs.get("columns") else ",".join(kwargs["columns"])
        condition = "1" if not kwargs.get("where") else f'{kwargs["where"]}'
        values = [kwargs.get("values")] if isinstance(kwargs.get("values"), str) else kwargs.get("values")
        query = f"SELECT {columns} FROM {table} WHERE {condition};"
    log_sqlite(query), log_sqlite(values) if values else log_sqlite(query)

    try:
        rows = db.execute(query, values).fetchall() if values else db.execute(query).fetchall()
    except sqlite3.Error as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_msgs = traceback.format_exception(exc_type, exc_value, exc_tb)
        if isinstance(tb_msgs, list):
            tb_msgs = ''.join(tb_msgs).splitlines()
        err = {
            f'SQLite.{e.__class__.__name__}': f'{" ".join(e.args)}',
            'Debug Info': {
                "query": query,
                "kwargs": kwargs,
                "parsed": {"table": table, "columns": columns, "condition": condition, "values": values}
            },
            'SQLite Traceback': tb_msgs
        }
        # logger.error(err)
        return err

    if rows:
        if ((len(rows) == 1) and (not kwargs.get("force"))):
            return dict(rows[0])
        return [dict(row) for row in rows]
    return False

###############################################################################
#                              UPDATE OPERATIONS                              #
###############################################################################
def updateRow(db, query="", **kwargs):
    """
    Update data in the database

    ARGS:
        Required - db (object)          - the database connection object
        Optional - query (str)          - a complete SQL query

        Required - table (str)          - the table to update data
        Required - columns (list)       - the columns to edit
        Required - col_values (list)    - the values for the columns
        Required - where (str)          - conditional "WHERE" statement
        Required - values (str|list)    - the value(s) for the "WHERE" statement
    RETURNS:
        num_edits (int) OR False - the number of rows that were edited

    EXAMPLE: with [query]
        num_edits = updateRow(db, query="UPDATE users SET username=? WHERE (user_id=6);")

    EXAMPLE: with [query] and [col_values] and [values]
        num_edits = updateRow(db,
                                query="UPDATE users SET username=? WHERE (user_id=?);",
                                col_values=["user_06"], values=["6"])

    EXAMPLE: with [params] directly
        num_edits = updateRow(db, table="users", columns=["username"], col_values=["user_06"],
                                where="user_id=?", values=["6"])

    EXAMPLE: with [params] as (dict)
        username = "user_06"
        params = {
            "table": "users",
            "columns": ["username"],
            "col_values": [username],
            "where": "user_id=?",
            "values": [username],
        }
        num_edits = updateRow(db, **params)
    """
    if query:
        table = ""
        columns = []
        condition = ""
        col_values = kwargs.get("col_values")
        values = [kwargs.get("values")] if isinstance(kwargs.get("values"), str) else kwargs.get("values")
    else:
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        columns, col_values = parseColumnValues(kwargs["columns"], kwargs["col_values"])
        condition = f'({kwargs["where"]})'
        values = [kwargs["values"]] if isinstance(kwargs["values"], str) else kwargs["values"]
        query = f"UPDATE {table} SET {columns} WHERE {condition};"
    log_sqlite(query), log_sqlite(col_values), log_sqlite(values) if (col_values and values) else log_sqlite(query)

    try:
        cur = db.execute(query, col_values+values) if (col_values or values) else db.execute(query)
    except sqlite3.Error as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_msgs = traceback.format_exception(exc_type, exc_value, exc_tb)
        if isinstance(tb_msgs, list):
            tb_msgs = ''.join(tb_msgs).splitlines()
        err = {
            f'SQLite.{e.__class__.__name__}': f'{" ".join(e.args)}',
            'Debug Info': {
                "query": query,
                "kwargs": kwargs,
                "parsed": {
                    "table": table, "columns": columns, "col_values": col_values,
                    "condition": condition, "values": values
                }
            },
            'SQLite Traceback': tb_msgs
        }
        # logger.error(err)
        return err

    return cur.rowcount

###############################################################################
#                              DELETE OPERATIONS                              #
###############################################################################
def deleteRow(db, query="", **kwargs):
    """
    Delete row(s) from the database

    ARGS:
        Required - db (object)          - the database connection object
        Optional - query (str)          - a complete SQL query
        Required - table (str)          - the table to delete data from
        Required - where (str)          - conditional "WHERE" statement
        Required - values (str|list)    - the value(s) for the "WHERE" statement
    RETURNS:
        num_delets (int) OR False - the number of rows that were deleted

    EXAMPLE: with [query]
        num_deletes = deleteRow(db, query="DELETE FROM users WHERE (user_id=6);")

    EXAMPLE: with [query] and [values]
        num_deletes = deleteRow(db, query="DELETE FROM users WHERE (user_id=?);", values=["6"])

    EXAMPLE: with [params] directly
        num_deletes = deleteRow(db, table="users", where="user_id=?", col_values=["6"])

    EXAMPLE: with [params] as (dict)
        user_id = 6
        params = {
            "table": "users", "where": "user_id=?", "values": user_id,
        }
        num_deletes = deleteRow(db, **params)
    """
    if query:
        table = ""
        condition = ""
        values = [kwargs["values"]] if isinstance(kwargs["values"], str) else kwargs["values"]
    else:
        # table = kwargs.get("table")
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        condition = f'({kwargs["where"]})'
        values = [kwargs["values"]] if isinstance(kwargs["values"], str) else kwargs["values"]
        query = f"DELETE FROM {table} WHERE {condition};"
    log_sqlite(query), log_sqlite(values) if values else log_sqlite(query)

    try:
        cur = db.execute(query, values)
    except sqlite3.Error as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb_msgs = traceback.format_exception(exc_type, exc_value, exc_tb)
        if isinstance(tb_msgs, list):
            tb_msgs = ''.join(tb_msgs).splitlines()
        err = {
            f'SQLite.{e.__class__.__name__}': f'{" ".join(e.args)}',
            'Debug Info': {
                "query": query, "kwargs": kwargs, "parsed": {
                    "table": table, "condition": condition, "values": values
                }
            },
            'SQLite Traceback': tb_msgs
        }
        # logger.error(err)
        return err

    return cur.rowcount

###############################################################################
#                               Helper Functions                              #
###############################################################################
# DB Functions ################################################################
def addTable(db, query="", **kwargs):
    if not query:
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        columns = kwargs.get("columns")
        query = f'CREATE TABLE {table} ({", ".join(columns)});'
    log_sqlite(query)
    try:
        cur = db.execute(query)
    except (sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
        # log_sqlite(e.args)
        return {"SQLite_Error": e.args, "query": query, "columns": columns, "kwargs": kwargs}
    return {"message": f"{abs(cur.rowcount)} table created", "table": table, "columns": columns}

def deleteTable(db, query="", **kwargs):
    if not query:
        table = kwargs["table"]["name"] if isinstance(kwargs.get("table"), dict) else kwargs.get("table")
        query = f"DROP TABLE {table};"
    log_sqlite(query)
    try:
        cur = db.execute(query)
    except (sqlite3.ProgrammingError, sqlite3.OperationalError) as e:
        # log_sqlite(e.args)
        return {"SQLite_Error": e.args, "query": query, "kwargs": kwargs}
    return {"message": f"{abs(cur.rowcount)} table deleted!"}

def getTable(db, tables=[], table_name=''):
    if not tables:
        tables = getTables(db)
    table = dict(*filter(lambda t: t["name"] == table_name, tables))
    if table:
        table["info"] = {c["name"]: c["type"] for c in table["columns"]}
        table["columns"] = {c["name"]: c["type"].split()[0] for c in table["columns"]}
    return table

def getTables(db):
    args = {
        "table": 'sqlite_schema', "columns": ["name", "type"], "where": "type = ? AND name NOT LIKE ?",
        "values": ['table', 'sqlite_%'], "force": True,
    }
    tables = fetchRows(db, **args)
    for table in tables:
        table["columns"] = getColumns(db, table)
    return tables

def getColumns(db, table, required=False, editable=False, non_editable=False, ref=False):
    if not table.get("columns"):
        query = f'PRAGMA table_info({table["name"]});'
        rows = db.execute(query).fetchall()
        col_info = []
        for row in [dict(row) for row in rows]:
            dflt = row["dflt_value"]
            info = {"name": row["name"], "type": f'{row["type"]} {"PRIMARY KEY" if row["pk"] else ""}'}
            info["type"] += f'{"NOT NULL"}' if row["notnull"] else ""
            info["type"] += f" DEFAULT ({dflt})" if dflt else ""
            col_info.append(info)
        return col_info

    regex = r"(PRIMARY KEY|DEFAULT)"
    editable_columns = {key: table["columns"][key] for key in table["columns"] if not re.search(regex, table["info"][key])}
    non_editable_columns = {key: table["columns"][key] for key in table["columns"] if re.search(regex, table["info"][key])}

    if required or editable:
        return editable_columns
    if non_editable:
        return non_editable_columns
    if ref:
        return re.search(r"(.*_id)", " ".join(non_editable_columns)).group()
    return table["columns"]

###############################################################################
#                              Utility Functions                               #
###############################################################################
def securePassword(plaintext):
    salt = os.urandom(32)
    digest = hashlib.pbkdf2_hmac("sha256", plaintext.encode(), salt, 1000)
    hex_salt = codecs.encode(salt, "hex").decode()
    hex_digest = digest.hex()
    hex_pass = hex_salt + hex_digest
    return hex_pass

def checkPassword(plaintext, hex_pass):
    hex_salt = hex_pass[:64]
    hex_digest = hex_pass[64:]
    salt = codecs.decode(hex_salt, "hex")
    digest = codecs.decode(hex_digest, "hex")
    test_digest = hashlib.pbkdf2_hmac("sha256", plaintext.encode(), salt, 1000)
    if test_digest == digest:
        return True
    return False

class User(object):
    def __init__(self):
        self.user_id = None
        self.cookiedata = request.get_cookie("user_id", secret=secret_key)
        if self.cookiedata:
            self.user_id = self.cookiedata
            self.token = genToken("user_id", self.user_id, secret_key)
    def login(self, cookiedata):
        return response.set_cookie("user_id", cookiedata, secret=secret_key)

def require_uid(fn):
    def check_uid(**kwargs):
        if request.get_cookie("user_id", secret=secret_key):
            return fn(**kwargs)
        else:
            error_http = HTTPError(401, "Unauthorized")
            error_http.message = {
                "Unauthorized": "Invalid Token - Missing Session Cookie",
                "message": "Please provide a session cookie or valid token."
            }
            return error_http
    return check_uid

def uploadImage(url):
    # -- load image mimetypes
    mimetypes.init()

    # -- check if 'static/img' path exists
    img_path = py_path.parent.joinpath('static', 'img')
    if not img_path.exists():
        # -- img_path doesn't exist, creating img_path and css_path (just in case)...
        img_path.mkdir(parents=True)
        img_path.with_stem('css').mkdir(exist_ok=True)

    # -- count existing images...
    name = len(list(img_path.iterdir())) + 1

    # -- download image from url
    try:
        req = requests.get(url)
    except Exception:
        return {"Python_Error": f"Failed to download image from url: {url}"}

    # -- determine image mimetype
    ext = mimetypes.guess_extension(req.headers["Content-Type"])
    if not ext:
        ext = next((m for m in mimetypes.guess_all_extensions(req.headers["Content-Type"])), None)
    if not ext:
        return {"MimeType_Error": f"Failed to Detect Mime Type for Image: {name}{Path(url).suffix}"}

    # -- exporting image to img_path
    img_file = img_path.joinpath(f'{name}{ext}')
    with open(str(img_file), 'wb') as f:
        f.write(req.content)

    # -- extract full path relative to web root '/'
    full_path = Path(f'/{img_file.relative_to(img_file.parents[2])}')
    msg = "image url uploaded"
    return {"message": msg, "url": url, "full_path": str(full_path), 'file_name': full_path.name}

###############################################################################
#                                   Parsers                                   #
###############################################################################
def extract(info, cols):
    return{k: v for k, v in {c.values() for c in info} if k in cols}

def mapUrlPaths(url_paths, req_items, table=""):
    # dt = "DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
    dt = "NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime'))"
    r = re.compile(r"/", re.VERBOSE)
    keys = map(str.lower, r.split(url_paths)[::2])
    vals = map(str.upper, r.split(url_paths)[1::2])
    url_params = dict(zip(keys, vals))

    # -- process params
    req_params = {k.lower():v.upper() for (k,v) in req_items.items()}
    params = {**url_params, **req_params}

    # -- order and build columns for CREATE statement
    prime_key = False
    id_cols, time_cols, non_cols, rejects = ([] for i in range(4))
    for (k, v) in params.items():
        if re.match(r"([a-z_0-9]+_id)", k):
            if ((table == "users") or ("user" not in k)) and prime_key == False:
                id_cols.insert(0, f"{k} {v} PRIMARY KEY")
                prime_key = True
            else:
                id_cols.append(f"{k} {v} NOT NULL")
        elif re.match(r"([a-z_0-9]+_time)", k):
            time_cols.append(f"{k} {v} {dt}")
        elif re.match(r"([a-z_0-9]+)", k):
            non_cols.append(f"{k} {v} NOT NULL")
        else:
            reject.append({k: v})

    columns = id_cols + non_cols + time_cols
    response.debug.append({"mapUrlPaths()": {"__params__": params, "__columns__": columns}})
    return params, columns

def parseURI(url_paths):
    r = re.compile(r"/", re.VERBOSE)
    url_split = r.split(url_paths)
    # print(f'url_paths = {url_paths}')
    # print(f'url_split = {url_split}')

    if (len(url_split) % 2) == 0:
        p = map(str, url_split)
        url_params = dict(zip(p, p))
    elif url_paths:
        keys, values = ([] for i in range(2))
        for i in range(0, len(url_split), 2):
            if re.match(r"([a-z_]+)", url_split[i]):
                keys.append(url_split[i])
                values.append(url_split[i + 1])
            else:
                values[-1] = "/".join([values[-1], url_split[i]])
        url_params = dict(zip(keys, values))
    else:
        url_params = {}

    return url_params

def parseUrlPaths(url_paths, req_items, columns):
    # -- parse "params" and "filters" from url paths
    url_params = parseURI(url_paths)

    # -- process filters (pop from url_params if necessary)
    url_filters = url_params.pop("filter") if url_params.get("filter") else ""
    req_filters = req_items["filter"] if req_items.get("filter") else ""
    filters = " AND ".join([f for f in [url_filters, req_filters] if f])

    # -- process params
    req_params = {k:v for (k,v) in req_items.items() if k in columns}
    params = {**url_params, **req_params}

    return params, filters

def parseFilters(filters, conditions, values):
    regex = r"""
        ("|')(?P<val>[^"|^']*)("|')             # wrapped in single or double quotations
    """
    r = re.compile(regex, re.VERBOSE)
    f_conditions = r.sub("?", filters)

    filter_conditions = f_conditions if not conditions else " AND ".join([conditions, f_conditions])
    filter_values = values + [m.groupdict()["val"] for m in r.finditer(filters)]
    logger.debug(f'filter_conditions: "{filter_conditions}"')
    logger.debug(f'filter_values: {filter_values}')

    return filter_conditions, filter_values

def parseColumnValues(cols, vals):
    columns = ""
    col_values = []
    # -- check for expressions containing "column name"
    for i, expression in enumerate([any([col in val for col in cols]) for val in vals]):
        if expression:
            columns += f"{cols[i]}={vals[i]}, "
        else:
            columns += f"{cols[i]}=?, "
            col_values.append(vals[i])
    columns = columns.strip(", ")

    logger.debug(f"columns: '{columns}'")
    logger.debug(f"col_values: {col_values}")
    return columns, col_values

py_path = get_py_path()
secret_key = py_path.parent.name
print(f'py_path: {py_path}')
def parseParams(secret_key):
    params = {}
    if request.json:
        params.update(request.json)
    r_key = ""
    for k in request.params.keys():
        if (("{" in k) and ("}" in k)):
            try:
                params.update(json.loads(k))
                r_key = k
            except Exception:
                logger.error(f'ERROR: k = {k}')
    if r_key:
        try:
            request.params.pop(r_key)
        except Exception:
            logger.error(f'ERROR: r_key = {r_key}')
    request.params.update(params)
    for k, v in request.params.items():
        if k == "token":
            try:
                # print(f'cookie_info = {cookie_decode(b64decode(v), secret_key)}')
                logger.info(f'cookie_info = {cookie_decode(b64decode(v), secret_key)}')
                cookie_info = dict([cookie_decode(b64decode(v), secret_key)])
                for kk, vv in cookie_info.items():
                    request.cookies.update({kk: b64decode(v).decode()})
                # request.headers.update({"Cookie": f'user_id="{b64decode(v)}"'})
            except Exception as e:
                logger.error(e)
                logger.error(f'ERROR: {k} = {v}')


def genToken(name='', value='', secret_key=Path.cwd().parent.name):
    return b64encode(cookie_encode((name, value), secret_key)).decode()

###############################################################################
#                                   Logging                                    #
###############################################################################
def checkUserAgent():
    user_agent = request.environ["HTTP_USER_AGENT"] if request.environ.get("HTTP_USER_AGENT") else ""
    browser_agents = [
        "Mozilla",
        "Firefox",
        "Seamonkey",
        "Chrome",
        "Chromium",
        "Safari",
        "OPR",
        "Opera",
        "MSIE",
        "Trident",
    ]
    print(f'user_agent = {user_agent}')
    regex = r"({})".format("|".join(browser_agents))

    if re.search(regex, user_agent):
        # print({"user-agent": user_agent})
        return True
    return False

def clean(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, FormsDict) or isinstance(v, WSGIHeaderDict):
                data.update({k: dict(v)})

    str_data = json.dumps(data, default=str, indent=2)
    # if checkUserAgent():
    #     return template("templates/prettify.tpl", data=str_data)
    cleaned = json.loads(str_data)
    return cleaned

# -- https://stackoverflow.com/questions/31080214/python-bottle-always-logs-to-console-no-logging-to-file
def getLogger():
    project = py_path.parent.name
    print(f'project: {project}')

    logger = logging.getLogger(f'logs/{project}.py')
    logger.setLevel(logging.DEBUG)
    file_handler = TimedRotatingFileHandler(f'logs/{project}.log', when='midnight')
    formatter = logging.Formatter('%(msg)s')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def log_sqlite(query):
    request_time = datetime.now()
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR') or request.remote_addr
    status = "request"
    logger.info('%s %s %s %s %s' % (ip_address, request_time, request.method, request.url, status))
    logger.debug(query)


def log_to_logger(fn):
    '''
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    '''
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR') or request.remote_addr

        if isinstance(actual_response, dict):
            status = response.status if actual_response.get("status_code") == 200 else actual_response.get("status")
            logger.info('%s %s %s %s %s' % (ip_address, request_time, request.method, request.url, status))
            if not actual_response.get("message") == "available commands":
                logger.info(json.dumps({"request.params": dict(request.params)}))
                logger.info(json.dumps(actual_response, default=str, indent=2))
        elif response.status == 200 or isinstance(actual_response, str):
            status = 200
            logger.info('%s %s %s %s %s' % (ip_address, request_time, request.method, request.url, status))
        elif actual_response._status_code == 200:
            status = 200
            logger.info('%s %s %s %s %s' % (ip_address, request_time, request.method, request.url, status))
        else:
            try:
                logger.info("=== ATTEMPT TO CLEAN ERROR ===")
                logger.debug(actual_response.__str__)
                if not dict(actual_response.headers):
                    for k,v in actual_response.headerlist:
                        print(k, v)
                        actual_response.add_header(k, v)
                res = actual_response.__dict__
                if not res.get('body'):
                    res["body"] = res.get("_status_line'")
                    logger.info(inspect(res))
                err = ErrorsRestPlugin()
                res_err = err.cleanError(res)
            except Exception as e:
                logger.info("=== FAILED TO CLEAN ERROR ===")
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb_msgs = traceback.format_exception(exc_type, exc_value, exc_tb)
                if isinstance(tb_msgs, list):
                    tb_msgs = ''.join(tb_msgs).splitlines()
                res_err = {
                    f'{e.__class__.__name__}': f'{" ".join(e.args)}',
                    'Debug_Info': {
                        "ip_address": ip_address,
                        "args": args,
                        "kwargs": kwargs,
                        "request_url": request.url,
                    },
                    'Traceback': tb_msgs
                }
                logger.error(json.dumps(res_err, default=str, indent=2))
            return res_err
        return actual_response
    return _log_to_logger
logger = getLogger()


# ErrorRestPlugin #############################################################
class ErrorsRestPlugin(object):
    name = 'ErrorsRestPlugin'
    api = 2

    def __init__(self, dumps=json_dumps):
        """init()"""
        self.json_dumps = dumps

    def log(self, error_log):
        request_time = datetime.now()
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR') or request.remote_addr
        status = error_log.get('_status_line') if error_log.get('_status_code') != response.status_code else response.status
        logger.info('%s %s %s %s %s' % (ip_address, request_time, request.method, request.url, status))
        logger.info(self.json_dumps(error_log, default=str, indent=2))

    def cleanError(self, data):
        for k, v in data.items():
            if isinstance(v, FormsDict) or isinstance(v, WSGIHeaderDict):
                data.update({k: dict(v)})

        traceback = ""
        if isinstance(data.get("traceback"), str):
            data["traceback"] = data["traceback"].splitlines()
            traceback = data["traceback"][-1]
        error_key = "Python_Error" if data.get('_status_code') == 500 else "Error"
        error_msg = data.pop('message') if data.get('message') else {'message': data.get('body')}
        # error_msg = data.get('body') if isinstance(data.get('body'), dict) else {"Error": data.get('body')}
        error_log = {**error_msg, error_key: data}
        self.log(error_log)

        data.update({'traceback': traceback})
        error = {"message": error_msg, error_key: data}
        return self.json_dumps(error, default=str, indent=2)

    def setup(self, app):
        """Initialize Handler"""
        for plugin in app.plugins:
            if isinstance(plugin, JSONPlugin):
                self.json_dumps = plugin.json_dumps
                break

        if not self.json_dumps:
            self.json_dumps = json_dumps

        def default_error_handler(res):
            if res.content_type == "application/json":
                return res.body
            res.content_type = "application/json"

            return self.cleanError(res.__dict__)

        app.default_error_handler = default_error_handler

    def apply(self, callback, route):
        """Execute Handler"""
        return callback
