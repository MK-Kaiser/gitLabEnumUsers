#!/usr/bin/env python3
# Author: c0braKai
import requests, argparse
"""enumerates gitlab server for usernames"""


def openid_conf(url):
    """searches openid config file for interesting links"""
    print('searching for interesting pages in openid configuration')
    page = requests.get('http://'+ url + '/.well-known/openid-configuration')
    print('Auth:', page.json()['authorization_endpoint'])
    print('Token:', page.json()['token_endpoint'])
    print('UserInfo:', page.json()['userinfo_endpoint'])
    print('Key:', page.json()['jwks_uri'])

#def git_version():
    """determine gitlab version"""

def user_enum(url):
    """performs unauthenticated user enumeration"""
    names = []
    users = []
    fail = 0
    print('searching for users at:',url)

    try:
        for i in range(1, 200):
            page = requests.get('http://' + url + '/api/v4/users/' + str(i))
            if page.status_code == 200:
                print('User found!')
                names.append(page.json()['name'])
                users.append(page.json()['username'])

            else:
                fail += 1
                if fail == 5:
                    print('Usernames found:', users)
                    break
    except:
        for i in range(1, 200):
            page = requests.get('http://' + url + '/api/v3/users/' + str(i))
            if page.status_code == 200:
                print('User found!')
                names.append(page.json()['name'])
                users.append(page.json()['username'])

            else:
                fail += 1
                if fail == 5:
                    print('Usernames found:', users)
                    break

def main():
    parser = argparse.ArgumentParser(description='Provide a url to a gitlab server to enumerate user accounts')
    parser.add_argument('-v', '--version', dest='ver', required=False, action='store_true', help='display version number')
    parser.add_argument('-u', '--url', dest='url', type=str, help='provide a url')
    args = parser.parse_args()

    if args.ver:
        print('gitLabEnumUsers 0.1')
        exit(0)
    if args.url == None:
        print('Usage: python3 gleu.py -u gitlab.htb')
        exit(0)
    else:
        user_enum(args.url)
        openid_conf(args.url)


if __name__ == '__main__':
    main()
