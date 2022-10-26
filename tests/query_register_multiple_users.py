#!/usr/bin/env python3
import argparse
import query


def register(users=False):
    if users:
        # -- register 4 users
        for user in ['alice', 'bob', 'anna', 'steve']:
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


if __name__ == '__main__':
    base_url='https://bartender.hopto.org/'
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--register', default=False, action="store_true", help="call /register")
    ap.add_argument('-d', '--delete', default=False, action="store_true", help="call /delete")
    ap.add_argument('-e', '--examine', default=False, action="store_true", help="call /get")
    ap.add_argument('-u', '--users', required=False, action="store_true", help="table to perform action on")
    args = ap.parse_args()

    if args.register:
        register(users=args.users)
    if args.delete:
        delete(users=args.users)
    if args.examine:
        examine()
