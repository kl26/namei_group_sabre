'''
Created on Jan 10, 2016

@author: SG0946321
'''
from abc import abstractmethod

class Activity:
    
    @abstractmethod
    def runActivity(self, sharedContext):
        print("Implement me!")