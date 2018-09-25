'''
Created on Jan 7, 2016

@author: SG0946321
'''
from com.sabre.api.sacs.rest.AuthenticationCall import AuthenticationCall
from datetime import datetime, timedelta

class TokenHolder:
    
    token = None
    expirationDate = None
    
    def getToken(self):
        if TokenHolder.token is None or TokenHolder.expirationDate < datetime.now():
            print("renew the token")
            TokenHolder.token = AuthenticationCall().callForToken()
            TokenHolder.expirationDate = datetime.now() + timedelta(seconds=TokenHolder.token['expires_in'])
            
        return TokenHolder.token
    