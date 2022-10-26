#!/usr/bin/env python3
"""
usage: query.py [-h] [-u URL] query

positional arguments:
  query              api endpoint to query

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  base url of web framework

example usage:
    query.py '/get/users'
    query.py '/get/users' --url 'http://localhost:8080'
"""
# -- System Modules -- #
from urllib.parse import urlparse, parse_qsl
from pathlib import Path
import http.cookiejar
import argparse
import requests
import pickle
import json
import sys
import re

# -- for importing parent module
sys.path.append(str(Path('.').absolute().parent))

# -- Helper Modules -- #
from utils.db_functions import parseUrlPaths
from rich import print, print_json


def export_cookies(session, cookie_file="cookies.pickle"):
    """Export Session Cookies"""
    with open(cookie_file, "wb") as f:
        pickle.dump(session.cookies, f)

def export_headers(session, header_file="headers.pickle"):
    """Export Session Headers"""
    with open(header_file, "wb") as f:
        pickle.dump(session.headers, f)

def load_cookies(cookie_file="cookies.pickle"):
    """Load External Cookies"""
    with open(cookie_file, "rb") as f:
        return pickle.load(f)

def load_headers(header_file="headers.pickle"):
    """Load External Headers"""
    with open(header_file, "rb") as f:
        return pickle.load(f)

def getCode(text):
    if '?' in text:
        return 'erlang'
    if text.strip().startswith('/'):
        return 'jq'
    return 'rexx'

def parseQuery(query):
    commands = [
        "add",
        "get",
        "edit",
        "delete",
        "login",
        "logout",
        "status",
        "register",
        "createTable",
        "deleteTable",
        "uploadImageUrl"
    ]
    tables = [
        "users",
        "bartenders",
        "bartender_shifts",
        "bartender_wages",
        "managers",
        "restaurant_photos",
        "restaurant_profile",
        "restaurant_requests",
        "restaurant_schedule"
    ]
    regex = rf"""
    /({'|'.join(commands)})/({'|'.join(tables)}) |  # catch /<cmd>/<table_name
    /({'|'.join(commands)})                      # catch only /<cmd>
    """
    m = re.compile(regex, re.VERBOSE)
    if not m.search(query):
        return None

    endpoint = "/" + "/".join([term for term in m.search(query).groups() if term])
    query_trimmed = query.replace(endpoint, "")
    url_paths = urlparse(query_trimmed).path.strip("/")
    query_params = dict(parse_qsl(urlparse(query_trimmed).query))

    # print(f'endpoint = "{endpoint}"')
    # print(f'url_paths = "{url_paths}"')
    # print(f'query_params = "{query_params}"')

    params, filters = parseUrlPaths(url_paths, query_params, list(query_params.keys()))
    arguments = "\n".join([f"{k} = {v}" for (k, v) in params.items()])
    if filters and not params.get('filter'):
        return f"{arguments}\nfilter = {filters}"
    return arguments

def executeQuery(base_url, query):
    base_url = base_url.strip('/')
    url = f'{base_url}{query}'
    arguments = parseQuery(query)
    arg_code = getCode(arguments)
    req_code = getCode(query)

    s = requests.Session()
    s.headers.update(load_headers())
    s.cookies.update(load_cookies())
    r = s.get(url)
    res = r.json() if r.status_code == 200 else r.text

    output = f"""
Arguments:
```{arg_code}
{arguments}
```

Request:
```{req_code}
{base_url+query}
```

Response:
```json"""
    print(output)
    print_json(data=res)
    print('```')
    return res

def main():
    examples = '''example usage:
    ./%(prog)s '/get/users'
    ./%(prog)s '/get/users' --url 'http://localhost:8888'
    '''

    ap = argparse.ArgumentParser(epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('query', help="api endpoint to query")
    ap.add_argument('-u', '--url', default="https://bartender.hopto.org/", help='base url of web framework')
    ap.add_argument('-l', '--login', default=False, action="store_true", help="login and save session cookies...")
    args = ap.parse_args()

    if args.login:
        s = requests.Session()
        r = s.post('https://bartender.hopto.org/login', data={"username": "admin", "password": "admin"})
        export_headers(s)
        export_cookies(s)


    executeQuery(base_url=args.url, query=args.query)
    # print(out)

if __name__ == '__main__':
    sys.exit(main())
