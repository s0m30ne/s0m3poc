#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re
from zoomeye import zoomeye
import importlib
import time

class s0m3poc(object):
    def __init__(self):
        self.target = ''
        self.query = ''
        self.pages = 10
        self.facets = ''
        self.port = False
        self.payload = ''
        self.poc = None
        self.search_type = 'host'

    def output(self, content):
        print "-- %s" % content

    def getInput(self, description = ''):
        content = raw_input("> %s" % description)
        return content

    def welcome(self):
        print """
        ------- WELCOME TO ----------------------------------
        |   ---    ---   --   --  ---   ---     ---    ---  |
        |  /   \  /   \  | \ / |     |  |  \   /   \  /     |
        |  \___   |   |  |  |  |   __|  |---|  |   |  |     |
        |      \  |   |  |     |     |  |      |   |  |     |
        |  \___/  \___/  |     |  ___|  |      \___/  \___  |
        |___________________________________________________|
        """

    def help(self):
        print """
  ---------------------------------------------------------------------------
  | You can choose your poc to test some targets through this little tool.  |
  | These targets can be either a single ip(url) or some ips(urls) searched |
  | through zoomeye.                                                        |
  |-------------------------------------------------------------------------|
  | If you want to search targets through zoomeye:                          |
  |-------------------------------------------------------------------------|
  | set query <query>        | set the query would search through zoomeye   |
  |-------------------------------------------------------------------------|
  | set pages <pagenum>      | set the page num would serch, default is 10. |
  | set facets <facets>      | set return columns. Default is only IP.      |
  | set port <True or False> | set reruen ip with or without port num.      |
  |                          | for example: 127.0.0.1:22. Default is False  |
  |-------------------------------------------------------------------------|
  | If you want to test for a single ip or url:                             |
  |-------------------------------------------------------------------------|
  | set target <target>      | set the ip or url to test                    |
  |-------------------------------------------------------------------------|
  | set search_type web|host | select to search hosts or websites           |
  |-------------------------------------------------------------------------|
  | set payload <payload>    | select which poc file to use.                |
  |-------------------------------------------------------------------------|
  | show options             | show what have been configured.              |
  |-------------------------------------------------------------------------|
  | show payloads            | show all payloads that can be used.          |
  |-------------------------------------------------------------------------|
  | exploit                  | begin to test targets.                       |
  |-------------------------------------------------------------------------|
  | exit                     | exit the program.                            |
  ---------------------------------------------------------------------------
        """

    def showOptions(self):
        self.output("query : %s" % self.query)
        self.output("pages : %d" % self.pages)
        self.output("facets : %s" % self.facets)
        self.output("port : %s" % self.port)
        self.output("target : %s" % self.target)
        self.output("payload : %s" % self.payload)
        self.output("search_type : %s" % self.search_type)

    def showPayloads(self):
        payload_path = "%s/payloads/" % os.getcwd()
        payloads = os.listdir(payload_path)
        for payload in payloads:
            if payload == "__init__.py":
                pass
            elif payload.endswith('.py'):
                self.output(payload[:-3])

    def setPara(self, name, value):
        if name == "query":
            self.query = value
        elif name == "pages":
            try:
                self.pages = int(value)
            except:
                self.output("[!] pages should be a num!")
        elif name == "facets":
            self.facets = value
        elif name == "port":
            if value == "True" or value == "true":
                self.port = True
            elif value == "False" or value == "false":
                self.port = False
            else:
                self.output("[!] page should be True or False")
        elif name == "target":
            self.target = value
        elif name == "search_type":
            if value == "host" or value == "web":
                self.search_type = value
            else:
                self.output("[!] You can only set search_type with host or web")
        elif name == "payload":
            if os.path.exists("./payloads/%s.py" % value):
                self.payload = value
                payload_path = "%s/payloads/" % os.getcwd()
                if not payload_path in sys.path:
                    sys.path.append(payload_path)
                if not self.payload in sys.modules:
                    self.poc = __import__(self.payload)
                else:
                    self.output("[!] please do not use system module name as your payload name!")
            else:
                self.output("[!] the payload %s doesn't exist!" % value)

    def exploit(self):
        if not self.payload:
            self.output("[!] please config the payload first!")
        else:
            if self.query:
                z = zoomeye.Zoomeye("wangjinzhenh@163.com", "waxh1314!")
                try:
                    z.run(self.poc.exploit, self.query, pages = self.pages, facets = self.facets, port = self.port, search_type = self.search_type)
                    while z.isReady():
                        time.sleep(1)
                except KeyboardInterrupt,e:
                    self.output("[!] user abort! Waiting for payload to stop...")
                    z.Done = True
                    while not z.queue.empty():
                        tmp = z.queue.get()
            elif self.target:
                try:
                    self.poc.exploit(self.target)
                except KeyboardInterrupt,e:
                    self.output("[!] user abort!")
            else:
                self.output("[!] please config target or zoomeye query first!")

    def run(self):
        self.welcome()
        while True:
            cmd = self.getInput()
            if cmd == "help":
                self.help()
            elif cmd == "show options":
                self.showOptions()
            elif cmd == "show payloads":
                self.showPayloads()
            elif re.search(r'set (?:query|pages|facets|port|target|payload|search_type) .+', cmd):
                paraList = re.findall(r'set (query|pages|facets|port|target|payload|search_type) (.+)', cmd)
                self.setPara(paraList[0][0], paraList[0][1])
            elif cmd == "exploit":
                self.exploit()
            elif cmd == "exit":
                sys.exit()
            elif cmd == "":
                pass
            else:
                self.output("[!] wrong command!")

if __name__ == '__main__':
    s0m3 = s0m3poc()
    s0m3.run()
