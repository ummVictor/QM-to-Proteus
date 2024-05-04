def findDestination(transition):
    # Importing processxml locally
    from processxml import stateObjList
    
    #Split destination string into list of strings
    ls = transition.destination.split("/") 
    #Retrieve end of list
    trans_index = ls[-1]
    #Check if last element is a number
    if(trans_index.isnumeric()):
        #Find the corresponding state in state list
        return (stateObjList[int(trans_index) - 1])
    #Last element is the string ".." so we have a self transition
    else:
        return "self"
    
    
class State:
    def __init__(self, stateName, entryA, exitA, transitions):
        self.stateName = stateName
        self.entry = entryA
        self.exit = exitA
        self.transitions = transitions
    def __str__(self):
        return f"{self.stateName}"

#Creates an transition object with a trigger object and destination state
#"trigger" should be a Trigger object
class Transition:
    def __init__(self, trigger, destination):
        self.trigger = trigger
        self.destination = destination
    def __str__(self):
        return f"Transition --> {findDestination(self)}, triggered by {self.trigger.triggerName}"

#Creates a trigger object with trigger Name
class Trigger:
    def __init__(self, triggerName):
        self.triggerName = triggerName
    def __str__(self):
        return f"{self.triggerName}"