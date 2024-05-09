import xml.etree.ElementTree as ET
import unittest


#Next issue: Store how the states connects to each other 
#   (list of string names for list of states and events) 
#   (connections are displayed in map format, tuple arrays of entries)

tree = ET.parse('statemachine.qm')
root = tree.getroot()

stateParseList = []
stateObjList = []
trigParseList = []
trigObjList = []
tranParseList = []
tranObjList = []
#currentStateTransitions = []

#Method to find which state a transition is pointing to using the state list ordering, will not work for hsms.
#Takes in a transition object and returns either a state object or "self", indicating a self transition
def findDestination(transition):
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

#Currently Creates a state object with a state name, entry action, and exit action
#Need to a add a list of transitions objects which start at this state object
#For future work into HSMs, states need a list of substates, and a reference to its smallest superstate
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

def traverse(element):
    currentStateTransitions = [] #A list to store current state transitions, in case a state has multiple transitions or none

    #Check if element is the initial transition, print the initial transition target
    if element.tag == 'initial':
        print('Initial Target:', element.attrib.get('target'))
    #If element is a state tag, get and print the state name, then check its children
    elif element.tag == 'state':
        state_name = element.attrib.get('name', 'Unnamed State')
        stateParseList.append(state_name) #Add to the list of states
        #print('State:', state_name)
        
        for child in element:
            #See if child of element is an entry action
            if child.tag == 'entry':
                global entry_action
                entry_action = child.text.strip() if child.text else ''
                #print('  Entry Action:', entry_action)
            #see if child of element is an exit action
            elif child.tag == 'exit':
                global exit_action
                exit_action = child.text.strip() if child.text else ''
                #print('  Exit Action:', exit_action)
            #See if child of element is a transition, if so find its name, target and trigger
            elif child.tag == 'tran':
                transition_target = child.attrib.get('target', 'Unknown Target') #Identify target
                tranParseList.append(transition_target) #Add transition target
                transition_trig = child.attrib.get('trig') #Identify trigger
                trigParseList.append(transition_trig) #Add transition trigger
                #print('  Transition Target:', transition_target)
                #print('  Transition trig:', transition_trig)
                trig = Trigger(transition_trig) #Create trigger object out of xml tag
                trnsit = Transition(trig, transition_target) #create transition obj using the transition trigger and its destination

                currentStateTransitions.append(trnsit)
            


        #Add state name, entry action and exit action to State Object
        st = State(state_name, entry_action, exit_action, currentStateTransitions)
        #Add state to global list of states
        stateObjList.append(st)
        #Reset list of saved state transitions
        currentStateTransitions = []

    for child in element:
        traverse(child)

traverse(root)

