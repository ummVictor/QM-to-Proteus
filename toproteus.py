from processxml import trigParseList, stateObjList
from cxml import findDestination
# Open a text file in write mode
def writeProteus():
    with open('output.proteus', 'w') as f:
        # Write Proteus header
        f.write("//Proteus\n\n")

        # Write beginning of the List of Triggers/Events
        f.write("//beginning of the List of Triggers/Event\n")
        for trigger_name in trigParseList:
            # Ensure consistent format for triggers
            if trigger_name.endswith("()"):
                f.write(f"event {trigger_name}\n")
            else:
                f.write(f"event {trigger_name};\n")
        f.write("//end of the List of Triggers/Event\n\n")

        # Write actor block with actor name 'learn'
        f.write("actor learn{\n")

        # Write statemachine block
        f.write("    statemachine {\n")
        
        # Write the initial state as 'initial Locked;'
        f.write("        initial Locked;\n")
        
        # Iterate through state object list to write state blocks
        for state in stateObjList:
            # Write state name
            f.write(f"        state {state.stateName} {{\n")
            
            # Iterate through each transition in the state
            for transition in state.transitions:
                trigger_name = transition.trigger.triggerName
                # Find the destination state
                destination_state = findDestination(transition)
                
                # Write the transition block
                f.write(f"            on {trigger_name} {{\n")
                f.write(f"                go {destination_state};\n")
                f.write(f"            }}\n")
            
            # Close the state block
            f.write("        }\n")
        
        # Close statemachine and actor blocks
        f.write("    }\n")
        f.write("}\n")
