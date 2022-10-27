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
    arguments = parseQuery(query)
    arg_code = getCode(arguments)
    req_code = getCode(query)

    s = requests.Session()
    s.headers.update(load_headers())
    s.cookies.update(load_cookies())
    r = s.get(url)
    res = r.json() if r.status_code == 200 else r.text

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
        output += '{\n'
        for key in res.keys():
            obj = res.get(key)
            if isinstance(obj, list):
                if len(obj) == 1:
                    output += f'  "{key}": {obj},\n'.replace("'", '"')
                else:
                    output += f'  "{key}": [\n'
                    for item in obj:
                        output += f'    {item},\n'.replace("'", '"')
                    output += '  ],\n'
            elif isinstance(obj, dict):
                output += f'  "{key}": [{obj}],\n'.replace("'", '"')
            else:
                output += f'  "{key}": "{obj}",\n'.replace("'", '"')
        output += '}\n```'
        print(output)

def main():
    examples = '''example usage:
    ./%(prog)s '/get/users'
    ./%(prog)s '/get/users' --url 'http://localhost:8888'
    '''

    ap = argparse.ArgumentParser(epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('query', help="api endpoint to query")
    ap.add_argument('-u', '--url', default="https://bartender.hopto.org/", help='base url of web framework')
    ap.add_argument('-s', '--short', default=True, action="store_false", help='json output length')
    ap.add_argument('--stdout', default=True, action="store_false", help="print output")
    ap.add_argument('-l', '--login', default=False, action="store_true", help="login and save session cookies...")
    ap.add_argument('--username', default='admin', help="used with [--login]")
    ap.add_argument('--password', default='admin', help="used with [--login]")
    args = ap.parse_args()

    if args.login:
        s = requests.Session()
        r = s.post('https://bartender.hopto.org/login', data={"username": args.username, "password": args.password})
        export_headers(s)
        export_cookies(s)
        args.query = f"/login/username/{args.username}/password/{args.passwordMMM}"

    executeQuery(base_url=args.url, query=args.query, short=args.short, stdout=args.stdout)
    # print(out)

if __name__ == '__main__':
    sys.exit(main())
