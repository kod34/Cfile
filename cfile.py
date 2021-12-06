#!/usr/bin/env python3

import subprocess, time, sys, threading, getopt
from pynput import keyboard
from stem import Signal
from stem.control import Controller
from datetime import datetime

combination = {'k','h','b','z'}
page = ''

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   CWHITE  = '\33[37m'

def banner():
    banner = color.BOLD+color.PURPLE+'''
  ____   __  _  _       
 / ___| / _|(_)| |  ___ 
| |    | |_ | || | / _ \
| |___ |  _|| || ||  __/
 \____||_|  |_||_| \___|
                        
\t\t            {0}by {3}kod34
                        
'''.format(color.PURPLE, color.CWHITE, color.GREEN, color.RED, color.BLUE, color.DARKCYAN, color.CYAN)
    print(banner)



def msg(c):
    print("cfile.py [-t interval] (0: No interval)")
    sys.exit(c)

def init():
    try:
        cmd = subprocess.run(['tor', '-f', 'torrc']).stdout
        print(cmd)
    except KeyboardInterrupt:
        print('Manual interrupt')
        sys.exit(0)


def change_ip():
    global interval
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    cmd = subprocess.run(['torify', 'curl', 'ifconfig.me'], capture_output=True).stdout.decode()
    stamp = datetime.now().strftime("%H:%M:%S")
    print(color.RED+str(stamp)+" |"+color.CWHITE+" New ip: "+color.BLUE+str(cmd)+color.CWHITE)
    time.sleep(interval)
    change_ip()

def m_change(key):
    global page, combination
    try:
        if key.char in combination:
            page += key.char
            if page == 'khbz':
                with Controller.from_port(port = 9051) as controller:
                    controller.authenticate()
                    controller.signal(Signal.NEWNYM)
                cmd = subprocess.run(['torify', 'curl', 'ifconfig.me'], capture_output=True).stdout.decode()
                print("New ip: "+color.GREEN+str(cmd)+color.CWHITE)
                page=''
        else:
            page=''
    except:
        pass

def key():
    with keyboard.Listener(on_press=m_change) as listener:
        listener.join()

def strt():

    if interval == 0:
        t1 = threading.Thread(target=init, args=())
        t2 = threading.Thread(target=key, args=())

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        
    else:
        t1 = threading.Thread(target=init, args=())
        t2 = threading.Thread(target=change_ip, args=())
        t3 = threading.Thread(target=key, args=())

        t1.start()
        time.sleep(10)
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.start()

def main():
    global interval
    try:
        opts, args = getopt.getopt(sys.argv[1:],'t:')
    except getopt.error:
        sys.stdout = sys.stderr
        msg(1)
    if len(opts) == 0:
        msg(0)
    else:
        for opt, arg in opts:
            if opt in ['-t']:
                try:
                    interval = int(arg)
                except ValueError:
                    print("Value Error")
                    sys.exit(1)
            if opt in ['-h']:
                msg(0)
    strt()

if __name__ == '__main__':
    main()
