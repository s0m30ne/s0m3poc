#!/usr/bin/env python
# coding: utf-8

"""Zoomeye SDK to search the web space."""

import sys
import os
import json
import pycurl
import StringIO
from Queue import Queue
from urllib import quote
import threading
import time
import certifi

class Zoomeye(object):
    """Class to search the web space using zoomeye."""

    def __init__(self, username, password):
        self.USERNAME = username
        self.PASSWORD = password
        self.queue = Queue()
        self.API_TOKEN = None
        self.Done = False


    def _getToken(self):
        """Login and get the api token."""

        user_auth = '{"username": "%s","password": "%s"}' % (self.USERNAME, self.PASSWORD)
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(pycurl.URL, "https://api.zoomeye.org/user/login")
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.CUSTOMREQUEST, "POST")
        c.setopt(pycurl.POSTFIELDS, user_auth)
        c.perform()

        ReturnData = json.loads(b.getvalue())
        if ReturnData.has_key('error'):
            print "[!]%s: %s" % (ReturnData['error'], ReturnData['message'])
            sys.exit()

        self.API_TOKEN = ReturnData['access_token']
        b.close()
        c.close()

    def search(self, query, facets = '', pages = 10, search_type = 'host', port = False):
        """Function to execute searches and return the result."""

        self._getToken()
        if self.API_TOKEN == None:
            print "[!]please config your API_TOKEN using function getToken() first"
            sys.exit()

        query = quote(query)
        for page in range(1, pages+1):
            if not self.Done:
                url = "https://api.zoomeye.org/%s/search?query=%s&page=%s&facets=%s" % (search_type, query, page, facets)
                self._getInfo(url)
                self._manageOutput(facets, port)
            else:
                break

        self.Done = True

    def _manageOutput(self, facets, port):
        """Function to format the outputs."""

        if self.info:
            #print "[+]totally %d results found!" % self.info['total']
            for host in self.info['matches']:
                result = {}
                
                if host.has_key('site'):
                    result['site'] = host['site']
                else:
                    if port:
                        result['ip'] = "%s:%s" % (host['ip'], host['portinfo']['port'])
                    else:
                        result['ip'] = host['ip']

                if facets:
                    for facet in self.info['facets']:
                        if host.has_key(facet):
                            result[facet] = host[facet]
                        else:
                            for key in host.keys():
                                if isinstance(host[key], dict):
                                    if host[key].has_key(facet):
                                        result[facet] = host[key][facet]
                                        break
                            else:
                                result[facet] = ""

                self.queue.put(result)

    def accountInfo(self):
        """Function to get the information about your account."""

        self._getToken()
        if self.API_TOKEN == None:
            print "[!]please config your API_TOKEN using function getToken() first"
            sys.exit()

        while not self._getInfo("https://api.zoomeye.org/resources-info"):
            pass

        return self.info

    def _getInfo(self, url):
        """Function to request for the information."""

        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.CUSTOMREQUEST, "GET")
        c.setopt(pycurl.HTTPHEADER, ['Authorization: JWT %s' % self.API_TOKEN.encode()])
        c.perform()
        
        self.info = json.loads(b.getvalue())
        if self.info.has_key('error'):
            print "[!]%s: %s" % (self.info['error'], self.info['message'])
            sys.exit()

    def run(self, fun, query, facets = '', pages = 10, search_type = 'host', port = False):
        """Do what you want to do with the function you defined."""

        threads = []
        t1 = threading.Thread(target = self.search, args = (query, facets, pages, search_type, port))
        threads.append(t1)
        t2 = threading.Thread(target = fun, args = (self,))
        threads.append(t2)

        for t in threads:
            t.setDaemon(True)
            t.start()

        while not self.Done:
            try:
                time.sleep(0.1)
            except:
                print '[!]User aborted, wait all slave threads to exit...'
                self.Done = True

    def isReady(self):
        """Return the state of the zoomeye SDK"""

        if not self.queue.empty() or not self.Done:
            return True
        else:
            return False