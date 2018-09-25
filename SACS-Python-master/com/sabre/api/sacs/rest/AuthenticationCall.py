'''
Created on Jan 7, 2016

@author: SG0946321
'''
import json
import requests
import base64
import com.sabre.api.sacs.config.Configuration as conf

class AuthenticationCall:
    
    def callForToken(self):
        config = conf.Configuration()
        headers = {
            'Authorization' : "Basic " + self.buildCredentials(),
            'Accept' : '*/*'
        }
        response = requests.post(config.getProperty("environment") + "/v2/auth/token", headers=headers, data={"grant_type" : "client_credentials"})
        return json.loads(response.text)
    
    def buildCredentials(self):
        config = conf.Configuration()
        credentials = config.getProperty("formatVersion") + ":" + \
            config.getProperty("userId") + ":" + \
            config.getProperty("group") + ":" + \
            config.getProperty("domain")
        secret = self.b64(config.getProperty("clientSecret"))
        return self.b64(self.b64(credentials) + ":" + secret)
            
    def b64(self, toEncode):
        return base64.b64encode(toEncode.encode('utf-8')).decode("utf-8")