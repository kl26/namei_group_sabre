'''
Created on Jan 10, 2016

@author: SG0946321
'''
from com.sabre.api.sacs.workflow.Activity import Activity
from com.sabre.api.sacs.rest.BaseRestCall import BaseRestPostCall
import com.sabre.api.sacs.config.Configuration as conf

class BargainFinderMaxActivity(Activity):
    def __init__(self, departureDate, returnDate, origin, destination, tripType, passengerCount, passengerType, cabinType, preferLevel, segmentType):
        self.departureDate = departureDate
        self.returnDate = returnDate
        self.origin = origin
        self.destination = destination
        self.tripType = tripType
        self.passengerCount = passengerCount
        self.passengerType = passengerType
        self.cabinType = cabinType
        self.preferLevel = preferLevel
        self.segmentType = segmentType

    def runActivity(self, sharedContext):
        print("BargainFinderMax")
        sharedContext.departureDate = self.departureDate
        sharedContext.returnDate = self.returnDate
        sharedContext.origin = self.origin
        sharedContext.destination = self.destination
        sharedContext.tripType = self.tripType
        sharedContext.passengerCount = self.passengerCount
        sharedContext.passengerType = self.passengerType
        sharedContext.cabinType = self.cabinType
        sharedContext.preferLevel = self.preferLevel
        sharedContext.segmentType = self.segmentType

        config = conf.Configuration()

        response = BaseRestPostCall(config.getProperty("environment") + "/v4.3.0/shop/flights?mode=live", self.createRequest(sharedContext)).executeCall()
        sharedContext.bargainFinderMaxResult = response
        return None
    
    def createRequest(self, sharedContext):
        requestObject = {
            "OTA_AirLowFareSearchRQ": {
                "Target": "Production",                                 # Used to indicate whether the request is for the Test or Production system.
                    "POS": {                                            # Point of sale object.
                        "Source": [{
                            "PseudoCityCode" : "",
                            "RequestorID": {
                                "Type": "1",
                                "ID": "1",
                                "CompanyName": {}
                            }
                        }]
                    },
                    "OriginDestinationInformation": [{
                        "RPH": "1",                                     #placeholder for OriginDestinationInformation 
                        "DepartureDateTime": sharedContext.departureDate+"T03:00:00",
                        "OriginLocation": {
                            "LocationCode": sharedContext.origin
                        },
                        "DestinationLocation": {
                            "LocationCode": sharedContext.destination
                        },
                        "TPA_Extensions": {                             #Trading Partner Agreement (TPA)
                            "SegmentType": {
                                "Code": sharedContext.segmentType       #"Code" can be "ARUNK", "O" for normal, or "X" for connection.
                            }
                        }
                    }],
                    "TravelPreferences": {
                        "ValidInterlineTicket": True,
                        "CabinPref": [{
                            "Cabin": sharedContext.cabinType,           #Premium First (P) First (F) Premium Business (J) Business (C) Premium Economy (S) Economy (Y)
                            "PreferLevel": sharedContext.preferLevel    #Valid values are: 'Only', 'Unacceptable', 'Preferred'.
                        }],
                        "TPA_Extensions": {
                            "TripType": {
                                "Value": sharedContext.tripType         # 'OneWay', 'Return', 'Circle', 'OpenJaw', 'Other'.
                            },
                            "LongConnectTime": {
                                "Min": 780,
                                "Max": 1200,
                                "Enable": True
                            },
                            "ExcludeCallDirectCarriers": {
                                "Enabled": True                         #Force DSF to return schedules only for carriers bookable by Sabre.
                            }
                        }
                    },
                    "TravelerInfoSummary": {
                        "SeatsRequested": [sharedContext.passengerCount], #The sum of all seats required by all passenger groups.
                        "AirTravelerAvail": [{
                            "PassengerTypeQuantity": [
        
                            ]}
                        ]
                    },
                    "TPA_Extensions": {
                        "IntelliSellTransaction": {
                            "RequestType": {
                                "Name": "50ITINS"                       # 50ITINS, 100ITINS and 200ITINS.
                            }
                        }
                    }
                }
            }

        if self.tripType != 'OneWay':
            returnTrip = {
                "RPH": "2",                                             #placeholder for OriginDestinationInformation 
                "DepartureDateTime": sharedContext.returnDate+"T11:00:00",
                "OriginLocation": {
                    "LocationCode": sharedContext.destination
                },
                "DestinationLocation": {
                    "LocationCode": sharedContext.origin
                },
                "TPA_Extensions": {                                     #Trading Partner Agreement (TPA)
                    "SegmentType": {
                        "Code": sharedContext.segmentType               #"Code" can be "ARUNK", "O" for normal, or "X" for connection.                            }
                    }
                }
            }
            requestObject['OTA_AirLowFareSearchRQ']['OriginDestinationInformation'].append(returnTrip)

        if self.passengerType != 'N/A':
            types = []
            for key, value in self.passengerType.items():
                newType = {
                    "Code" : key, 
                    "Quantity" : value
                }
                types.append(newType)
            requestObject['OTA_AirLowFareSearchRQ']['TravelerInfoSummary']['AirTravelerAvail'][0]['PassengerTypeQuantity'] = types 
        return requestObject
