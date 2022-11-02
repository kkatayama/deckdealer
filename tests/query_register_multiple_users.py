#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.append(str(Path(sys.path[0]).parent))
from utils.paths import get_py_path
import argparse
import random
import query
import time
import re


def register(users=False):
    if users:
        # -- register 6 users
        for user in ['dealer', 'alice', 'bob', 'anna', 'steve']:
            q = f'/register/username/{user}/password/{user}/password2/{user}'
            print('---')
            query.executeQuery(base_url=base_url, query=q)
        print('---')

def delete(users=False):
    if users:
        # -- delete 6 users
        for user in ['dealer', 'alice', 'bob', 'anna', 'steve']:
            q = f'/delete/users/username/{user}'
            print('---')
            query.executeQuery(base_url=base_url, query=q)
        print('---')

def examine():
    table_names = [t['name'] for t in query.executeQuery(base_url=base_url, query='/get', stdout=False)["tables"]]
    for name in table_names:
        print(f'#### `{name}` table:')
        query.executeQuery(base_url=base_url, query=f'/get/{name}', short=False)

def createDeck(create=False):
    if create:
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
    if create:
        for card in deck:
            key = card["key"]
            name = card["name"]
            suit = card["suit"]
            desc = card["description"]
            fn = card["file_name"]
            q = f'/add/cards/key/{key}/name/{name}/suit/{suit}/description/{desc}/file_name/{fn}'
            query.executeQuery(base_url=base_url, query=q, short=True)
            time.sleep(0.25)
        return
    return deck

def shuffleDeck(deck):
    q = '/createTable/deck/card_id/INTEGER/key/TEXT/name/TEXT/suit/TEXT/description/TEXT/file_name/TEXT/entry_time/DATETIME'
    query.executeQuery(base_url=base_url, query=q, short=True)

    for card in random.sample(deck, 52):
        key = card["key"]
        name = card["name"]
        suit = card["suit"]
        desc = card["description"]
        fn = card["file_name"]
        q = f'/add/deck/key/{key}/name/{name}/suit/{suit}/description/{desc}/file_name/{fn}'
        query.executeQuery(base_url=base_url, query=q, short=True)
        time.sleep(0.25)

def deleteTables():
    table_names = [t['name'] for t in query.executeQuery(base_url=base_url, query='/get', stdout=False)["tables"]]
    for name in table_names:
        if name not in ['users', 'cards', 'deck']:
            print(f'#### `{name}` table:')
            query.executeQuery(base_url=base_url, query=f'/deleteTable/{name}', short=False)

def createTables():
    for name in ["players", "spectators", "games", "active_game", "score_board"]:
        q = f'/createTable/{name}'
        if name == "players":
            q += '/player_id/INTEGER/user_id/INTEGER/game_id/INTEGER/name/TEXT/email/TEXT/entry_time/DATETIME'
        if name == "spectators":
            q += '/spectator_id/INTEGER/user_id/INTEGER/game_id/INTEGER/name/TEXT/email/TEXT/entry_time/DATETIME'
        if name == "games":
            q += '/game_id/INTEGER/name/TEXT/min_players/TEXT/max_players/TEXT/min_decks/TEXT/max_decks/TEXT/player_actions/TEXT/rules/TEXT/entry_time/DATETIME'
        if name == "active_game":
            q += '/entry_id/INTEGER/game_id/INTEGER/user_id/INTEGER/player_id/INTEGER/player_hand/TEXT/player_action/TEXT/entry_time/DATETIME'
        if name == "score_board":
            q += '/score_id/INTEGER/game_id/INTEGER/user_id/INTEGER/player_id/INTEGER/winner/TEXT/winner_email/TEXT/winner_hand/TEXT/winner_score/INTEGER/players/TEXT/player_hands/TEXT/player_scores/TEXT/spectators/TEXT/entry_time/DATETIME'
        query.executeQuery(base_url=base_url, query=q, short=True)

if __name__ == '__main__':
    domain = re.search(r'[a-z]+', get_py_path().parent.name).group().replace('bartend', 'bartender')
    base_url = f'https://{domain}.hopto.org'

    ap = argparse.ArgumentParser()
    ap.add_argument('--register', default=False, action="store_true", help="call /register")
    ap.add_argument('--delete', default=False, action="store_true", help="call /delete")
    ap.add_argument('--examine', default=False, action="store_true", help="call /get")
    ap.add_argument('--users', required=False, action="store_true", help="table to perform action on")
    ap.add_argument('--createDeck', required=False, action="store_true", help='call /createDeck')
    ap.add_argument('--shuffleDeck', required=False, action="store_true", help='call /shuffleDeck')
    ap.add_argument('--createTables', required=False, action="store_true", help='call /createTables')
    ap.add_argument('--deleteTables', required=False, action="store_true", help='call /deleteTables')
    args = ap.parse_args()

    if args.register:
        register(users=args.users)
    if args.delete:
        delete(users=args.users)
    if args.examine:
        examine()
    if args.createDeck:
        createDeck(create=True)
    if args.shuffleDeck:
        deck = createDeck(create=False)
        shuffleDeck(deck)
    if args.createTables:
        createTables()
    if args.deleteTables:
        deleteTables()
