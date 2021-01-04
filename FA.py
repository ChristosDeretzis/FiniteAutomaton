from collections import defaultdict
import sys

class FAe:

    def __init__(self, states, transitions, start_state, accept_states, num_transitions):
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state
        self.num_transitions = num_transitions
        self.alphabet = set()

    def transition_to_next_state(self, input_value):
        next_states = set()
        e_states, last_used_states = set(), set()

        for state in self.current_state:
            e_states.add(state)
            set_difference = e_states - last_used_states

            while bool(set_difference):
                set_difference = e_states - last_used_states

                if not bool(set_difference):
                    break
                last_used_states = e_states.copy()

                for state in set_difference:
                    if (state, '@') in self.transitions.keys():
                        e_states = e_states | self.transitions[(state, '@')]

            for state in e_states:
                next_states = next_states | self.transitions[(state, input_value)]

        self.current_state = self.current_state | e_states if input_value == ' ' else next_states


    def is_state_accepted(self):
        for i in self.current_state:
            if i in self.accept_states:
                return True
        return False

    def move_to_initial_state(self):
        self.current_state = self.start_state
        return

    def calculate_alphabet(self):
        self.alphabet.add(" ")
        for y in self.transitions.keys():
            if y[1] not in self.alphabet:
                self.alphabet.add(y[1])

    def run_automaton(self, inputList):
        self.move_to_initial_state()
        self.calculate_alphabet()

        inputList.append(' ')
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
