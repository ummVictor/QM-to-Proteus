from cxml import findDestination

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