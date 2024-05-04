from processxml import trigParseList, stateObjList
from classes import findDestination

def writeProteus():
    with open('output.proteus', 'w') as f:
        # Write Proteus header
        f.write("//Proteus\n\n")

        # Write beginning of the List of Triggers/Events
        f.write("//beginning of the List of Triggers/Event\n")
        written_triggers = set()  # Keep track of written triggers
        for trigger_name in trigParseList:
            # Ensure consistent format for triggers and avoid duplication
            if trigger_name.endswith("()") and trigger_name not in written_triggers:
                f.write(f"event {trigger_name}\n")
                written_triggers.add(trigger_name)
            elif trigger_name not in written_triggers:
                f.write(f"event {trigger_name};\n")
                written_triggers.add(trigger_name)
        f.write("//end of the List of Triggers/Event\n\n")

        # Write actor block with actor name 'learn'
        f.write("actor learn{\n")

        # Write statemachine block
        f.write("    statemachine {\n")
        
        # Write the initial state as 'initial Locked;'
        f.write("        initial Locked;\n")
        
        written_states = set()  # Keep track of written states
        # Iterate through state object list to write state blocks
        for state in stateObjList:
            # Write state name if not already written
            if state.stateName not in written_states:
                f.write(f"        state {state.stateName} {{\n")
                written_states.add(state.stateName)
            
                # Iterate through each transition in the state
                for transition in state.transitions:
                    trigger_name = transition.trigger.triggerName
                    # Find the destination state
                    destination_state = findDestination(transition)
                    
                    # Write the transition block with proper indentation
                    f.write(f"            on {trigger_name} {{\n")
                    f.write(f"                go {destination_state};\n")
                    f.write(f"            }}\n")
                
                # Close the state block
                f.write("        }\n")
        
        # Close statemachine and actor blocks
        f.write("    }\n")
        f.write("}\n")

writeProteus()
