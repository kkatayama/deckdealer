#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append(str(Path(sys.path[0]).parent))
from utils.paths import get_py_path
import argparse
import query
import time
import re


def register(users=False):
    if users:
        # -- register 4 users
        for user in ['ellan', 'jimmy']:  # ['alice', 'bob', 'anna', 'steve']:
            q = f'/register/username/{user}/password/{user}/password2/{user}'
            print('---')
            query.executeQuery(base_url=base_url, query=q)
        print('---')

def delete(users=False):
    if users:
        # -- delete 4 users
        for user in ['alice', 'bob', 'anna', 'steve']:
            q = f'/delete/users/username/{user}'
            print('---')
            query.executeQuery(base_url=base_url, query=q)
        print('---')

def examine():
    table_names = [t['name'] for t in query.executeQuery(base_url=base_url, query='/get', stdout=False)["tables"]]
    for name in table_names:
        print(f'#### `{name}` table:')
        query.executeQuery(base_url=base_url, query=f'/get/{name}', short=False)

def createDeck():
    q = '/createTable/cards/card_id/INTEGER/key/TEXT/name/TEXT/suit/TEXT/description/TEXT/file_name/TEXT/entry_time/DATETIME'
    query.executeQuery(base_url=base_url, query=q, short=True)

    cards = []
    for img in sorted(get_py_path().parent.parent.joinpath('image_tests', 'PNG-cards-1.3').glob('*.png')):
        if re.search(r'(?P<name>[0-9]+|jack|queen|king|ace)_of_(?P<suit>\w+)', img.name) and '2.png' not in str(img):
            r = re.search(r'(?P<name>[0-9]+|jack|queen|king|ace)_of_(?P<suit>\w+)', img.name)
            name = r.groupdict()["name"]
            name = name.upper()[:1] if name.isalpha() else name
            suit = r.groupdict()["suit"].upper()[:1]
            key = f'{name}{suit}'
            c_name = img.name.split('_', maxsplit=1)[0].upper()
            c_suit = r.groupdict()["suit"].upper()
            desc = img.name.replace('.png', '')
            fn = f'{key}.png'
            cards.append({'key': key, 'name': c_name, 'suit': c_suit, 'description': desc, 'file_name': fn})

    deck = []
    deck += cards[4:36]
    deck += cards[0:4]
    deck += cards[40:44]
    deck += cards[48:52]
    deck += cards[44:48]
    deck += cards[36:40]
    for card in deck:
        key = card["key"]
        name = card["name"]
        suit = card["suit"]
        desc = card["description"]
        fn = card["file_name"]
        q = f'/add/cards/key/{key}/name/{name}/suit/{suit}/description/{desc}/file_name/{fn}'
        query.executeQuery(base_url=base_url, query=q, short=True)
        time.sleep(0.5)

if __name__ == '__main__':
    domain = re.search(r'[a-z]+', get_py_path().parent.name).group().replace('bartend', 'bartender')
    base_url = f'https://{domain}.hopto.org'

    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--register', default=False, action="store_true", help="call /register")
    ap.add_argument('-d', '--delete', default=False, action="store_true", help="call /delete")
    ap.add_argument('-e', '--examine', default=False, action="store_true", help="call /get")
    ap.add_argument('-u', '--users', required=False, action="store_true", help="table to perform action on")
    ap.add_argument('-c', '--createDeck', required=False, action="store_true", help='call /createDeck')
    args = ap.parse_args()

    if args.register:
        register(users=args.users)
    if args.delete:
        delete(users=args.users)
    if args.examine:
        examine()
    if args.createDeck:
        createDeck()
