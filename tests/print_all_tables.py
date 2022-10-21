#!/usr/bin/env python3
from query import load_cookies, load_headers, print
import requests
import json


url = "https://bartender.hopto.org/add"
s = requests.Session()
s.headers.update(load_headers())
s.cookies.update(load_cookies())
r = s.get(url)

print('\n<table>\n')
for table in r.json().get("tables")[1:]:
    name = table["name"]
    cols = [t["name"] for t in table["columns"]]
    # print(f'  * **`{name}`** | `{cols}` <br />'.replace("'", '"'))
    print('<tr><td> Table Name </td><td> Column Names </td></tr>')
    print(f'<tr><td>\n\n```rexx\n{name}\n```\n\n</td><td>\n\n```jq\n{cols}\n```\n\n</td></tr>'.replace("'", '"'))
print('</table>')
