from collections import defaultdict
import sys

class FAe:

    def __init__(self, transitions, transitions_e, start_state, accept_states, num_transitions):
        self.transitions = transitions
        self.transitions_e = transitions_e
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = set()
        self.num_transitions = num_transitions
        self.alphabet = set()

    def transition_to_next_state(self, input_value):
       temp_current_states = set()
       for cs in self.current_state.copy():
           for key_e, value_e in transitions_dict_e.items():
               if cs == key_e[0] and key_e[1] == '@':
                   self.current_state.remove(key_e[0])
                   for item in value_e:
                       temp_current_states.add(item)
           for key, value in transitions_dict.items():
               if key[1] == input_value and key[0] == cs:
                   for item in value:
                    temp_current_states.add(item)

       self.current_state.clear()
       self.current_state.update(temp_current_states)
       temp_current_states.clear()



    def is_state_accepted(self):
        for i in self.current_state:
            if i in self.accept_states:
                return True
        return False

    def calculate_alphabet(self):
        self.alphabet.add(" ")
        for y in self.transitions.keys():
            if y[1] not in self.alphabet:
                self.alphabet.add(y[1])

    def run_automaton(self, inputList):
        self.calculate_alphabet()
        self.current_state = set()
        self.current_state.add(self.start_state)

        for input in inputList:
            if input not in self.alphabet:
                print("The letter ({}) does not exist on the alphabet.".format(input))
                return False
            self.transition_to_next_state(input)
        return self.is_state_accepted()


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

        transitions_dict = {}
        transitions_dict_e = {}
        for line in file:
            line = line.split(" ")

            key = tuple([int(line[0]), line[1]])
            value = tuple([int(line[2])])

            if line[1] != "@":
                if key in transitions_dict.keys():
                    transitions_dict[key] = transitions_dict[key] + value
                else:
                    transitions_dict.update({
                        key: value
                    })
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
    automaton = FAe(transitions_dict, transitions_dict_e, start_state, final_states, number_of_transitions)

    while True:
        word = input("Enter a word: ")
        if word == 'exit':
            exit(0)
        accepted = automaton.run_automaton(word)
        if accepted:
            print("The word is accepted!")
        else:
            print("The word is not accepted")