'''
Created on Jan 10, 2016

@author: SG0946321
'''
from com.sabre.api.sacs.workflow.SharedContext import SharedContext

class Workflow:
    
    def __init__(self, startActivity):
        self.startActivity = startActivity
        
    def runWorkflow(self):
        nextActivity = self.startActivity
        sharedContext = SharedContext()
        while nextActivity is not None:
            nextActivity = nextActivity.runActivity(sharedContext)
        
        return sharedContext