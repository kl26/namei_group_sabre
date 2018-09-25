'''
Created on Nov 27, 2015

@author: SG0946321
'''
from com.sabre.api.sacs.rest.activities.LeadPriceCalendarActivity import LeadPriceCalendarActivity
from com.sabre.api.sacs.workflow.Workflow import Workflow

workflow = Workflow(LeadPriceCalendarActivity("LAX", "JFK", "2018-09-15"))
sharedContext = workflow.runWorkflow()
print("---------------------- RESULTS --------------------------")
print(sharedContext.leadPriceCalendarResult.text)
print(sharedContext.instaFlightResult.text)
print(sharedContext.bargainFinderMaxResult.text)