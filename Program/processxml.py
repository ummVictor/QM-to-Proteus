import xml.etree.ElementTree as ET
from classes import State, Transition, Trigger

# change the path to the path of your state diagram
tree = ET.parse(r'C:\Users\victo\Desktop\GIT\QM-to-Proteus\QM-to-Proteus\Program\statemachine.qm')
root = tree.getroot()

stateParseList = []
stateObjList = []
trigParseList = []
trigObjList = []
tranParseList = []
tranObjList = []


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

print("Number of States: ", len(stateParseList))
print("List of States: ", stateParseList)
print("List of Unnamed Transition Targets: ", tranParseList)
print("List of Triggers/Events: ", trigParseList)
print("StateObject list: ")
for i in stateObjList: #Loop through state list
    print(" " , i) #Print state
    for e in i.transitions: #Loop through current state's list of transitions
        print("\t", i, e)
print("end")