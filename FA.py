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
        transitions_dictionary = defaultdict(set)
        states = set()
        final_list = set()
        for line in file:
            split = line.split(" ")
            if split[0].startswith("states"):
                for i in range(int(split[1])):
                    states.add(i + 1)
            elif split[0].startswith("initial"):
                initial = int(split[1])
                temp = set()
                temp.add(initial)
                initial = temp
            elif split[0].startswith("final"):
                continue
            elif split[0].startswith("f_states"):
                for i in range(1, len(split)):
                    final_list.add(int(split[i]))
            elif split[0].startswith("transitions"):
                num_transitions = int(split[1])
            else:
                transitions_dictionary[(int(split[0]), split[1])].add(int(split[2]))

    return states, initial, final_list, transitions_dictionary, num_transitions

if __name__ == "__main__":
    filename = sys.argv[1]

    states, initial, accept_states, transitions, num_transitions = readDataFromFile(filename)
    automaton = FAe(states, transitions, initial, accept_states, num_transitions)
    input_program = list(input("Enter word: "))

    while(True):
        if (input_program[0] == 'exit'):
            print('Exiting program.')
            exit()
        print(automaton.run_automaton(input_program))
        input_program = list(input("Enter input :"))

