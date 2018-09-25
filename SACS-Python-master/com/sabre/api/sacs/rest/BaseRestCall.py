'''
Created on Jan 7, 2016

@author: SG0946321
'''

import requests
from com.sabre.api.sacs.rest.TokenHolder import TokenHolder

class BaseRestGetCall:

    def __init__(self, url, requestObject):
        self.requestObject = requestObject
        self.url = url
        self.tokenHolder = TokenHolder()
        print("base rest class constructor")
        
    def executeCall(self):
        print("executing GET call")
        headers = {'Authorization' : "Bearer " + self.tokenHolder.getToken()['access_token']}
        response = requests.get(self.url, headers=headers, params=self.requestObject)
        return response

class BaseRestPostCall:
    
    def __init__(self, url, requestObject):
        self.requestObject = requestObject
        self.url = url
        self.tokenHolder = TokenHolder()
        
    def executeCall(self):
        print("executing POST call")
        headers = {
            'Authorization' : "Bearer " + self.tokenHolder.getToken()['access_token'],
            'Accept' : '*/*',
            'Content-Type' : 'application/json'
        }
#         req = requests.Request('POST', self.url, headers=headers, json=self.requestObject)
#         print(self.requestObject)
#         prepared = req.prepare()
#         
#         print('{}\n{}\n{}\n\n{}'.format('---START---', prepared.method + ' ' + prepared.url, '\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()), prepared.body))
#         s = requests.Session();
#         response = s.send(prepared)
        response = requests.post(self.url, headers=headers, json=self.requestObject)
        return response
        