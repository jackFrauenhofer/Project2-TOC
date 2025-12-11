from src.helpers.turing_machine import TuringMachineSimulator
from src.helpers.turing_machine import DIR_L, DIR_R, BLANK, DIR_S



# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        initial_config = ["", self.start_state, input_string]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        accepted = False
        non_leaf_configs = 0
        total_transitions = 0

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
        
            # 1. Iterate through every config in current_level.
            for config in current_level:
                left_stack, curr_state, right_stack = config

            # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if curr_state == self.accept_state:
                    print("\n")
                    print(f"Accepted! String was accepted in {depth} steps with the config: {config}")
                    self.print_tree(tree, total_transitions, non_leaf_configs)
                    accepted = True
                    return

            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                if curr_state == self.reject_state:
                    # print(f"Rejected! String was rejected in {depth} steps with the config: {config}") # Used for testing
                    continue # This just kills this particular branch and continues the loop

            # 4. If not Accept/Reject, find valid transitions in self.transitions.
                if len(right_stack) > 0:
                    head = right_stack[0]
                else:
                    head = BLANK
                transitions = self.get_transitions(curr_state, head) # this grabs the head to put into the fn given in frame code
                
                # Counts for degree of nondeterminism
                if len(transitions) >= 1:
                    non_leaf_configs += 1
                total_transitions += len(transitions)
            
            # 5. If no explicit transition exists, treat as implicit Reject.
                if not transitions: # if no transitions exist, just reject, so kill the branch
                    continue

                all_rejected = False # Have to set this to false because we must have found a transition
            
            # 6. Generate children configurations and append to next_level[cite: 148].

                for tran in transitions:
                    # This section does the writing part of the transition

                    symbol_to_write = tran['write'][0]
                    direction = tran['move'][0]
                    next_state = tran['next'] #Need the whole characters in the string

                    # This block updates the head and the right stack correctly
                    if len(right_stack) > 0: # check to make sure right stack is not empty
                        head = right_stack[0]
                        split_right_stack = right_stack[1:]
                    else: # If right stack empty, then head is blank and nothing on right stack
                        head = BLANK
                        right_stack = ""
                        split_right_stack = ""

                    if direction == DIR_L:
                        if len(left_stack) > 0:
                            moved_char = left_stack[-1]
                            next_left_stack = left_stack[:-1]
                            next_right_stack = moved_char + symbol_to_write + split_right_stack
                        else:
                            next_left_stack = ""
                            next_right_stack = BLANK + symbol_to_write + split_right_stack
                    
                    elif direction == DIR_R:
                        next_left_stack = left_stack + symbol_to_write
                        if len(split_right_stack) > 0:
                            next_right_stack = split_right_stack
                        else:
                            next_right_stack = ""

                    elif direction == DIR_S:
                        next_left_stack = left_stack
                        next_right_stack = symbol_to_write + split_right_stack # This returns the rewritten head to the right stack

                    # Use the below line to test the paths if needed
                    # print(f"Left: {next_left_stack}, Head: {next_right_stack[0]}, Right: {next_right_stack[1:]} and {curr_state} and {next_state}")
                
                    next_level.append([next_left_stack, next_state, next_right_stack])     
                        
            # Placeholder for logic:
            if not next_level and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"Rejected! String was rejected in {depth}")
                return

            tree.append(next_level)
            depth += 1

        self.print_tree(tree, total_transitions, non_leaf_configs)

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]

    def print_tree(self, tree, total_transitions, non_leaf_configs):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        print("\n")
        print(f"Degree of Nondeterminism: {total_transitions / non_leaf_configs}")
        print("---------------------- NTM Tree Depth Chart ----------------------")

        depth = 0
        for level in tree:
            print(f"At depth {depth}: ")
            depth += 1
            for config in level:
                left_stack, curr_state, right_stack = config
                print(f"Left Stack: {left_stack} | Current State: {curr_state} | Right Stack: {right_stack}")