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
sys.path.append(str(Path(sys.path[0]).parent))

# -- Helper Modules -- #
from utils.db_functions import parseUrlPaths
from utils.paths import get_py_path
from rich import print, print_json


def export_cookies(session='', cookie_file="cookies.pickle", py_path=''):
    """Export Session Cookies"""
    pickle.dump(session.cookies, py_path.joinpath(cookie_file).open('wb'))

def export_headers(session='', header_file="headers.pickle", py_path=''):
    """Export Session Headers"""
    pickle.dump(session.headers, py_path.joinpath(header_file).open('wb'))

def load_cookies(cookie_file="cookies.pickle", py_path=''):
    """Load External Cookies"""
    return pickle.load(py_path.joinpath(cookie_file).open('rb'))

def load_headers(header_file="headers.pickle", py_path=''):
    """Load External Headers"""
    return pickle.load(py_path.joinpath(header_file).open('rb'))

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
        "cards", "deck", "players", "spectators", "games", "active_game", "score_board",
        "users",
        "stuff",
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

    # print(f'params = {params}')
    # print(f'filters = {filters}')
    # print(f'arguments = {repr(arguments)}')

    if filters and not params.get('filter'):
        if arguments:
            return f"{arguments}\nfilter = {filters}"
        return f"filter = {filters}"
    return arguments

def executeQuery(base_url, query, short=True, stdout=True):
    base_url = base_url.strip('/')
    url = f'{base_url}{query}'

    if '/usage' not in query:
        arguments = parseQuery(query)
        arg_code = getCode(arguments)
        req_code = getCode(query)

    s = requests.Session()
    s.headers.update(load_headers(py_path=py_path))
    s.cookies.update(load_cookies(py_path=py_path))
    r = s.get(url)
    res = r.json() if r.status_code == 200 else r.text

    if '/usage' in query:
        print(res)
        return

    if not stdout:
        return res

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
```json
"""
    if short:
        print(output)
        print_json(data=res)
        print('```')
    else:
        tables = False
        if query in {'/get', '/add', '/edit', '/delete', '/createTable', '/deleteTable'}:
            tables = True
        output += '{\n'
        for key in res.keys():
            obj = res.get(key)
            if isinstance(obj, list):
                if len(obj) == 1:
                    output += f'  "{key}": {obj},\n'.replace("'", '"')
                else:
                    output += f'  "{key}": [\n'
                    for item in obj:
                        if tables:
                            print(item)
                        output += f'    {item},\n'.replace("'", '"')
                    output += '  ],\n'
            elif isinstance(obj, dict):
                output += f'  "{key}": [{obj}],\n'.replace("'", '"')
            else:
                output += f'  "{key}": "{obj}",\n'.replace("'", '"')
        output += '}\n```'
        if not tables:
            print(output)

def main(py_path):
    examples = '''example usage:
    ./%(prog)s '/get/users'
    ./%(prog)s '/get/users' --url 'http://localhost:8888'
    '''

    domain = re.search(r'[a-z]+', py_path.parent.name).group().replace('bartend', 'bartender')
    base_url = f'https://{domain}.hopto.org'

    ap = argparse.ArgumentParser(epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('query', help="api endpoint to query")
    ap.add_argument('-u', '--url', default=f"{base_url}/", help='base url of web framework')
    ap.add_argument('-s', '--short', default=True, action="store_false", help='json output length')
    ap.add_argument('--stdout', default=True, action="store_false", help="print output")
    ap.add_argument('-l', '--login', default=False, action="store_true", help="login and save session cookies...")
    ap.add_argument('--username', default='admin', help="used with [--login]")
    ap.add_argument('--password', default='admin', help="used with [--login]")
    args = ap.parse_args()

    if args.login:
        s = requests.Session()
        r = s.post(f'{base_url}/login', data={"username": args.username, "password": args.password})
        export_headers(session=s, py_path=py_path)
        export_cookies(session=s, py_path=py_path)
        args.query = f"/login/username/{args.username}/password/{args.password}"

    # print(args.url)
    executeQuery(base_url=args.url, query=args.query, short=args.short, stdout=args.stdout)
    # print(out)

py_path = get_py_path()
if __name__ == '__main__':
    sys.exit(main(py_path))
