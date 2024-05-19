import threading
import subprocess
import os
import requests
import time
import fade
from colorama import Fore
from distutils import spawn
x = '\033[0m'
b = '\033[1m'

try:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"                        made by {Fore.LIGHTCYAN_EX}{b}@missionarysex{x}")
    print('')
    if spawn.find_executable('node') is None:
        print(f" {Fore.RED}!{x}  {b}{Fore.YELLOW}node.js{x} {b}was not found, please install it first .{x}")
        exit(2)
    else:
        if os.path.isdir('node_modules'):
            pass
        else:
            print(f' {Fore.LIGHTCYAN_EX}[+]{x}  {b}installing {Fore.YELLOW}node.js{x} {b}modules ...{x}')
            os.system('npm install --silent')
            print('')
    while True:
        print(f"                {Fore.MAGENTA}[1]{x} {b}proxyless{x}            {Fore.MAGENTA}[2]{x} {b}with proxies")
        try:
            proxy_choice = int(input(f'   →{x}  {Fore.MAGENTA}~{x}  '))
            if proxy_choice > 2 or proxy_choice < 1:
                print(f' {Fore.RED}!{x} {b}invalid choice .{x}')
            else:
                break
        except ValueError:
            print(f' {Fore.RED}!{x} {b}invalid choice .{x}')

    try:
        with open('tokens.txt') as f:
            tokens = f.read().splitlines()
    except FileNotFoundError:
        print(f" {Fore.RED}!{x} {b}no {Fore.YELLOW}tokens.txt{x} {b}file found .{x}")
        exit()

    types = ['proxyless', 'with proxies']

    if len(tokens) < 1:
        print('')
        print(f" {Fore.RED}!{x}  {b}no tokens. {x}")
        print('')
        exit()
    print('')
    print(f" {Fore.MAGENTA}#{x}  {b}running {Fore.LIGHTCYAN_EX}{types[proxy_choice-1]}{x}{b} ...{x}")
    print(f" {Fore.MAGENTA}#{x}  {b}total tokens: {Fore.YELLOW}{len(tokens)}{x}")
    print('')

    if proxy_choice == 2:
        try:
            with open('proxies.txt') as f:
                proxies = f.read().splitlines()

            if len(proxies) < 1:
                print(f" {Fore.RED}!{x}  {b}no {Fore.YELLOW}proxies.txt{x} {b}file found .{x}")
                print(f" {Fore.RED}!{x}  {b}exiting ...{x}")
                print('')
                exit(2)
            else:
                print(f" {Fore.LIGHTCYAN_EX}[+]{x}  {b}total proxies:{x} {Fore.YELLOW}{len(proxies)}{x}")
                print('')
        except FileNotFoundError:
            print(f" {Fore.RED}!{x}  {b}no {Fore.YELLOW}proxies.txt{x} {b}file found .{x}")
            print(f" {Fore.RED}!{x}  {b}exiting ...{x}")
            print('')
            exit(2)

    procs = []
    for token in tokens:
        res = requests.get('https://discord.com/api/v9/users/@me', headers={ 'Authorization': token })
        if res.status_code != 200:
            print(f" {Fore.RED}[!]{x}  {b}invalid token :{x} {Fore.YELLOW}{token[:50]}...{x}")
            print('')
            pass
        command = ['node', '--no-deprecation', 'index.js', token, str(proxy_choice)]
        procs.append(subprocess.Popen(command))

    for p in procs:
        p.wait()
except KeyboardInterrupt:
    print('')
    print(f' {Fore.LIGHTCYAN_EX}[+]{x}  {b}exiting ...{x}')
    print('')
    exit(0)