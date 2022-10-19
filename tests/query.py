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
import argparse
import requests
import sys
import re

# -- for importing parent module
sys.path.append(str(Path('.').absolute().parent))

# -- Helper Modules -- #
from utils.db_functions import parseUrlPaths
from rich import print, print_json


def parseQuery(query):
    commands = [
        "add",
        "get",
        "edit",
        "delete",
        "login",
        "logout",
        "createTable",
        "deleteTable",
    ]
    tables = [
        "users",
        "oximeter"
    ]
    regex = rf"""
    /({'|'.join(commands)})/(tables) |  # catch /<cmd>/<table_name
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

    r = requests.get(url)
    res = r.json() if r.status_code == 200 else r.text

    output = f"""
Arguments:
```python
{arguments}
```

Request:
```ruby
{query}
```

Response:
```json"""
    print(output)
    print(res)
    print('```')
    return res

def main():
    examples = '''example usage:
    ./%(prog)s '/get/users'
    ./%(prog)s '/get/users' --url 'http://localhost:8080'
    '''

    ap = argparse.ArgumentParser(epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('query', help="api endpoint to query")
    ap.add_argument('-u', '--url', default="https://m2band.hopto.org/", help='base url of web framework')
    args = ap.parse_args()

    executeQuery(base_url=args.url, query=args.query)
    # print(out)

if __name__ == '__main__':
    sys.exit(main())
