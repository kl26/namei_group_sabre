'''
Created on Nov 27, 2015

@author: SG0946321
'''
from com.sabre.api.sacs.rest.activities.InstaFlightActivity import InstaFlightActivity
from com.sabre.api.sacs.rest.activities.BargainFinderMaxActivity import BargainFinderMaxActivity
from com.sabre.api.sacs.workflow.Workflow import Workflow
import json

departureDate = '2018-10-07'
returnDate = '2018-10-09'
origin = 'JFK'
destination = 'LAX'
tripType = 'OneWay'				#  'OneWay', 'Return', 'Circle', 'OpenJaw', 'Other'.
passengerCount = 2
passengerType = {'ADT': 2, 'INF' : 1}	
cabinType = 'Y'					#  Premium First (P) First (F) Premium Business (J) Business (C) Premium Economy (S) Economy (Y)
preferLevel = 'Preferred'		#  Valid values are: 'Only', 'Unacceptable', 'Preferred'.
segmentType = 'O' 				#  "Code" can be "ARUNK", "O" for normal, or "X" for connection.

workflow = Workflow(BargainFinderMaxActivity(departureDate, returnDate, origin, destination, tripType, passengerCount, 
	passengerType, cabinType, preferLevel, segmentType))
sharedContext = workflow.runWorkflow()

print("----------------------MAIN RESULTS --------------------------")

print(sharedContext)
#机票查询结果处理
raw_result_bargainFinderMax = json.loads(sharedContext.bargainFinderMaxResult.text, encoding='utf-8')

if 'errorCode' in raw_result_bargainFinderMax:
	print ('There is something wrong')
else:
# 需要提取信息：
# <td>出发日期</td>
# <td>出发机场</td>
# <td>到达日期</td>
# <td>到达机场</td>
# <td>中转站</td>
# <td>航空公司</td>
# <td>飞机型号</td>
# <td>航班号</td>
# <td>机舱类型</td>
# <td>飞行时间</td>
# <td>价格(USD)</td>
# <td>剩余座位</td>
	print ('Fine')
	# print (raw_result_bargainFinderMax)

	iti_index = 0
	iti_count = raw_result_bargainFinderMax["OTA_AirLowFareSearchRS"]["PricedItinCount"]

	iti_info = {}

	# print(iti_count)
	while iti_index < iti_count:	

		air_info = raw_result_bargainFinderMax["OTA_AirLowFareSearchRS"]["PricedItineraries"]["PricedItinerary"][iti_index]["AirItinerary"]
		price_info = raw_result_bargainFinderMax["OTA_AirLowFareSearchRS"]["PricedItineraries"]["PricedItinerary"][iti_index]["AirItineraryPricingInfo"]

		if air_info["DirectionInd"] == "Return":
			depart_info = air_info["OriginDestinationOptions"]["OriginDestinationOption"][0]
			return_info = air_info["OriginDestinationOptions"]["OriginDestinationOption"][1]
		else:
			depart_info = air_info["OriginDestinationOptions"]["OriginDestinationOption"][0]
			return_info = {}

		iti_info[iti_index] = {}
		iti_info[iti_index]["trip_type"] = air_info["DirectionInd"]
		iti_info[iti_index]["depart_info"] = depart_info
		iti_info[iti_index]["return_info"] = return_info
		iti_info[iti_index]["price_info"] = price_info[0]["ItinTotalFare"]
		iti_index += 1

	print(iti_info[0]["trip_type"])
	print("------------------------------------------------------------")
	print(iti_info[0]["depart_info"])
	print("------------------------------------------------------------")
	print(iti_info[0]["return_info"])
	print("------------------------------------------------------------")	
	print(iti_info[0]["price_info"])

		# departure_seg_count = raw_result_bargainFinderMax
		# return_seg_count = 
# #出发行程信息处理
# #TotalFare是往返费用和
# 		if departure_seg_count == 1:
# 			departure_itinerary_information[itinerary_index]['SegCount'] = 1
# 			departure_itinerary_information[itinerary_index]['DepartureTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["DepartureDateTime"]
# 			departure_itinerary_information[itinerary_index]['Origin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["DepartureAirport"]["LocationCode"]
# 			departure_itinerary_information[itinerary_index]['ArrivalTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["ArrivalDateTime"]
# 			departure_itinerary_information[itinerary_index]['Destination'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["ArrivalAirport"]["LocationCode"]
# 			departure_itinerary_information[itinerary_index]['Airline'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["MarketingAirline"]["Code"]
# 			departure_itinerary_information[itinerary_index]['TotalFare'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["ItinTotalFare"]["TotalFare"]["Amount"]
# 			departure_itinerary_information[itinerary_index]['RemainingSeats'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][0]["TPA_Extensions"]["SeatsRemaining"]["Number"]
# 			departure_itinerary_information[itinerary_index]['Cabin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][0]["TPA_Extensions"]["Cabin"]["Cabin"]
# 			departure_itinerary_information[itinerary_index]['AirEquipType'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["Equipment"]["AirEquipType"]
# 			departure_itinerary_information[itinerary_index]['FlightNumber'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]["FlightNumber"]
# 		else:
# 			departure_itinerary_information[itinerary_index]['SegCount'] = departure_seg_count
# 			departure_seg_index = 0
# 			total_time = 0
# 			remaining_seats = 999
			
# 			while departure_seg_index < departure_seg_count:
# 				departure_itinerary_information[itinerary_index][departure_seg_index] = {}
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['DepartureTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["DepartureDateTime"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['Origin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["DepartureAirport"]["LocationCode"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['ArrivalTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["ArrivalDateTime"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['Destination'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["ArrivalAirport"]["LocationCode"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['Airline'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["MarketingAirline"]["Code"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['FlightNumber'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["FlightNumber"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['AirEquipType'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["Equipment"]["AirEquipType"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['WaitingTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][departure_seg_index]["ElapsedTime"]
# 				departure_itinerary_information[itinerary_index][departure_seg_index]['Cabin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][departure_seg_index]["TPA_Extensions"]["Cabin"]["Cabin"]
# 				total_time +=  departure_itinerary_information[itinerary_index][departure_seg_index]['WaitingTime']
# 				current_seg_seats = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][departure_seg_index]["TPA_Extensions"]["SeatsRemaining"]["Number"]
# 				remaining_seats = min(remaining_seats, current_seg_seats)
# 				departure_seg_index += 1
				
# 			departure_itinerary_information[itinerary_index]['TotalFare'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["ItinTotalFare"]["TotalFare"]["Amount"]
# 			departure_itinerary_information[itinerary_index]['TotaTime'] = total_time
# 			departure_itinerary_information[itinerary_index]['RemainingSeats'] = remaining_seats
			
# #回程行程信息处理
# 		if return_seg_count == 1:
# 			return_itinerary_information[itinerary_index]['SegCount'] = 1
# 			return_itinerary_information[itinerary_index]['DepartureTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["DepartureDateTime"]
# 			return_itinerary_information[itinerary_index]['Origin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["DepartureAirport"]["LocationCode"]
# 			return_itinerary_information[itinerary_index]['ArrivalTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["ArrivalDateTime"]
# 			return_itinerary_information[itinerary_index]['Destination'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["ArrivalAirport"]["LocationCode"]
# 			return_itinerary_information[itinerary_index]['Airline'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["MarketingAirline"]["Code"]
# 			return_itinerary_information[itinerary_index]['TotalFare'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["ItinTotalFare"]["TotalFare"]["Amount"]
# 			return_itinerary_information[itinerary_index]['RemainingSeats'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][departure_seg_count]["TPA_Extensions"]["SeatsRemaining"]["Number"]
# 			return_itinerary_information[itinerary_index]['Cabin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][departure_seg_count]["TPA_Extensions"]["Cabin"]["Cabin"]
# 			return_itinerary_information[itinerary_index]['AirEquipType'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["Equipment"]["AirEquipType"]
# 			return_itinerary_information[itinerary_index]['FlightNumber'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]["FlightNumber"]
# 		else:
# 			return_itinerary_information[itinerary_index]['SegCount'] = return_seg_count
# 			return_seg_index = 0
# 			total_time = 0
# 			remaining_seats = 999
			
# 			while return_seg_index < departure_seg_count:
# 				return_itinerary_information[itinerary_index][return_seg_index] = {}
# 				return_itinerary_information[itinerary_index][return_seg_index]['DepartureTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["DepartureDateTime"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['Origin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["DepartureAirport"]["LocationCode"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['ArrivalTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["ArrivalDateTime"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['Destination'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["ArrivalAirport"]["LocationCode"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['Airline'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["MarketingAirline"]["Code"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['FlightNumber'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["FlightNumber"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['AirEquipType'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["Equipment"]["AirEquipType"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['WaitingTime'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][return_seg_index]["ElapsedTime"]
# 				return_itinerary_information[itinerary_index][return_seg_index]['Cabin'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][return_seg_index + departure_seg_count]["TPA_Extensions"]["Cabin"]["Cabin"]
# 				total_time +=  return_itinerary_information[itinerary_index][return_seg_index]['WaitingTime']
# 				current_seg_seats = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["FareInfos"]["FareInfo"][return_seg_index + departure_seg_count]["TPA_Extensions"]["SeatsRemaining"]["Number"]
# 				remaining_seats = min(remaining_seats, current_seg_seats)
# 				return_seg_index += 1
				
# 			return_itinerary_information[itinerary_index]['TotalFare'] = raw_result_instaFlights["PricedItineraries"][itinerary_index]["AirItineraryPricingInfo"]["ItinTotalFare"]["TotalFare"]["Amount"]
# 			return_itinerary_information[itinerary_index]['TotaTime'] = total_time
# 			return_itinerary_information[itinerary_index]['RemainingSeats'] = remaining_seats
# 		itinerary_index += 1
		
	#print (departure_itinerary_information)
	# print (departure_itinerary_information[0])
	# print (return_itinerary_information[0])

		


