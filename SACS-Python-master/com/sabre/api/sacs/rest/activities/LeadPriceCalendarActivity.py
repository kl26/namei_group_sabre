'''
Created on Jan 10, 2016

@author: SG0946321
'''
from com.sabre.api.sacs.workflow.Activity import Activity
from com.sabre.api.sacs.rest.activities.InstaFlightActivity import InstaFlightActivity
from com.sabre.api.sacs.rest.BaseRestCall import BaseRestGetCall
import com.sabre.api.sacs.config.Configuration as conf
#from test.test_decimal import ORIGINAL_CONTEXT

class LeadPriceCalendarActivity(Activity):
    
    def __init__(self, origin, destination, departureDate):
        self.origin = origin
        self.destination = destination
        self.departureDate = departureDate
    
    def runActivity(self, sharedContext):
        print("LeadPriceCalendar")
        sharedContext.origin = self.origin
        sharedContext.destination = self.destination
        sharedContext.departureDate = self.departureDate
        config = conf.Configuration()
        requestObject = {
            'origin' : self.origin,
            'destination' : self.destination,
            'lengthofstay' : 5,
            'pointofsalecountry' : 'US',
            'departuredate' : self.departureDate
        }
        response = BaseRestGetCall(config.getProperty("environment") + "/v2/shop/flights/fares", requestObject).executeCall() 
        sharedContext.leadPriceCalendarResult = response
        return InstaFlightActivity()