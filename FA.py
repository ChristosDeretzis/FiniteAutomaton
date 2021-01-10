from collections import defaultdict
import sys

class Automaton:

    def __init__(self, transitions, transitions_e, start_state, accept_states, num_transitions):
        self.transitions = transitions
        self.transitions_e = transitions_e
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = set()
        self.num_transitions = num_transitions
        self.alphabet = set()


    # This function checks all of the transitions in the
    # transitions dictionaries and checks the next states based on the
    # current state and the input character. If there is an e-transition,
    # remove the current state from the current state set.
    def  transition_to_next_state(self, input_value):
       temp_current_states = set()

       # loop the set in current state set
       for cs in self.current_state.copy():
           # check for e-transitions
           for key_e, value_e in transitions_dict_e.items():
               if cs == key_e[0] and key_e[1] == '@':
                   self.current_state.remove(key_e[0])
                   for item in value_e:
                       temp_current_states.add(item)
           for key, value in transitions_dict.items():
               if key[1] == input_value and key[0] == cs:
                   for item in value:
                    temp_current_states.add(item)

       # Update the current state set with the temporary
       # current state set
       self.current_state.clear()
       self.current_state.update(temp_current_states)
       temp_current_states.clear()


    # check if there is at least one
    # current state in the final state set
    def is_state_accepted(self):
        for i in self.current_state:
            if i in self.accept_states:
                return True
        return False

    # calculate the alphabet of the state
    # based on the second part of the transitions keys
    # and add the characters to the alphabet set
    def calculate_alphabet(self):
        self.alphabet.add(" ")
        for y in self.transitions.keys():
            if y[1] not in self.alphabet:
                self.alphabet.add(y[1])

    # run the automaton for a word by looping to its characters
    # and for each character transition to the next state
    # at the end of loop, check if the word belongs to the automaton
    def run_automaton(self, inputList):
        # Calculate the alphabet and add the start state to the current state
        self.calculate_alphabet()
        self.current_state = set()
        self.current_state.add(self.start_state)

        # for each letter in word check if the letter belongs to the alphabet and
        # calculate the current states for each letter. At the end of the for loop check
        # if there is at least one current state to the final states set
        for input in inputList:
            if input not in self.alphabet:
                print("The letter ({}) does not exist on the alphabet.".format(input))
                return False
            self.transition_to_next_state(input)
        return self.is_state_accepted()


# read the automaton from the .txt file
def readDataFromFile(fileName):
    with open(fileName) as file:
        number_of_states = int(file.readline())
        print("Number of states: ", number_of_states)
        print("--------------------------------------")

        start_state = int(file.readline())
        print("Start state: ", start_state)
        print("--------------------------------------")

        number_of_final_states = int(file.readline())
        print("Number of final states: ", number_of_final_states)
        print("--------------------------------------")

        final_states = set()
        final_states_str = file.readline();
        final_states_split = final_states_str.split(" ")
        for i in range(len(final_states_split)):
            final_states.add(int(final_states_split[i]))
        print("Final States: ", final_states)
        print("--------------------------------------")

        number_of_transitions = int(file.readline())
        print("Number of transitions: ", number_of_transitions)
        print("--------------------------------------")

        # for the transitions, create 2 dictionaries, 1 for the regular transitions
        # and the other for the e-transitions
        transitions_dict = {}
        transitions_dict_e = {}
        for line in file:
            line = line.split(" ")

            key = tuple([int(line[0]), line[1]])
            value = tuple([int(line[2])])

            # if the transition is not an e-transition, add it to the transitions dictionary
            if line[1] != "@":
                # if the key exists, add a value to the tuple
                # of the key: value pair
                if key in transitions_dict.keys():
                    transitions_dict[key] = transitions_dict[key] + value
                # create a new key: value pair to the dictionary
                else:
                    transitions_dict.update({
                        key: value
                    })
            # if the transition is an e-transition, add it to the transitions-e dictionary
            else:
                if key in transitions_dict_e.keys():
                    transitions_dict_e[key] = transitions_dict_e[key] + value
                else:
                    transitions_dict_e.update({
                        key: value
                    })
        print("Transitions : ", transitions_dict)
        print("Transitions of e: ", transitions_dict_e)

        return number_of_states, start_state, final_states, number_of_transitions, transitions_dict, transitions_dict_e



if __name__ == "__main__":
    filename = sys.argv[1]

    number_of_states, start_state, final_states, number_of_transitions, transitions_dict, transitions_dict_e = readDataFromFile(filename)
    automaton = Automaton(transitions_dict, transitions_dict_e, start_state, final_states, number_of_transitions)

    while True:
        word = input("Enter a word: ")
        if word == 'exit':
            exit(0)
        accepted = automaton.run_automaton(word)
        if accepted:
            print("The word is accepted!")
        else:
            print("The word is not accepted")