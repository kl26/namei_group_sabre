'''
Created on Jan 10, 2016

@author: SG0946321
'''
from com.sabre.api.sacs.workflow.Activity import Activity
from com.sabre.api.sacs.rest.BaseRestCall import BaseRestGetCall
import com.sabre.api.sacs.config.Configuration as conf
from com.sabre.api.sacs.rest.activities.BargainFinderMaxActivity import BargainFinderMaxActivity
import json

class InstaFlightActivity(Activity):
	def __init__(self, origin, destination, passengercount, departureDate, returnDate, includedcarriers = 'N/A', minfare = 'N/A', maxfare = 'N/A',
	inboundflightstops = 99, outboundflightstops = 99, limit = 10):
		self.origin = origin
		self.destination = destination
		self.departureDate = departureDate
		self.returnDate = returnDate
		self.includedcarriers = includedcarriers
		self.inboundflightstops = inboundflightstops
		self.outboundflightstops = outboundflightstops
		self.minfare = minfare
		self.maxfare = maxfare
		self.passengercount = passengercount
		self.limit = limit
    
	def runActivity(self, sharedContext):
		print("InstaFlightActivity")
		sharedContext.origin = self.origin
		sharedContext.destination = self.destination
		sharedContext.departureDate = self.departureDate
		sharedContext.returnDate = self.returnDate
		sharedContext.passengercount = self.passengercount
		config = conf.Configuration()
		requestObject = {
			'pointofsalecountry' : 'US',
			'limit' : self.limit,
			'origin' : self.origin,
			'destination' : self.destination,
			'departuredate' : self.departureDate,
			'returndate' : self.returnDate,
			'passengercount' : self.passengercount,
			'inboundflightstops' : self.inboundflightstops,
			'outboundflightstops' : self.outboundflightstops
		}
		if self.includedcarriers != 'N/A':
			requestObject['includedcarriers'] = self.includedcarriers
		if self.minfare != 'N/A':
			requestObject['minfare'] = self.minfare
		if self.maxfare != 'N/A':
			requestObject['maxfare'] = self.maxfare
			
		response = BaseRestGetCall(config.getProperty("environment") + "/v1/shop/flights", requestObject).executeCall() 
		sharedContext.instaFlightResult = response
		return None
