# coding: utf-8
from query import load_cookies, load_headers, print
import requests
import json


url = "https://bartender.hopto.org/add"
s = requests.Session()
s.headers.update(load_headers())
s.cookies.update(load_cookies())
r = s.get(url)

for table in r.json().get("tables")[1:]:
    name = table["name"]
    cols = [t["name"] for t in table["columns"]]
    print(f'  * **`{name}`** | `{cols}` <br />'.replace("'", '"'))
    
