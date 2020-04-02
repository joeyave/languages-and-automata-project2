import json
from itertools import chain
import pandas as pd

def epsilon_closure(transitions, state):
    closure = []
    if "eps" in transitions:
        closure.append(state)


class Nfa:
    def __init__(self, file_name):
        with open(file_name, 'r') as f:
            nfa_dict = json.load(f)

        self.states = nfa_dict['states']
        self.alphabet = nfa_dict['alphabet']
        self.transitions = {}
        for transition in nfa_dict['transitions']:
            self.transitions[(transition[0], transition[1])] = transition[2]
        self.initial_state = nfa_dict['initial_state']
        self.accepting_states = nfa_dict['accepting_states']

    def convert_to_dfa(self, file_name):
        dfa_alphabet = self.alphabet
        dfa_t_func = []
        dfa_initial_state = self.initial_state
        dfa_accepting_states = []
        dfa_states = [(dfa_initial_state,)]

        dfa_transitions = {}

        for dfa_state in dfa_states:
            for dfa_symbol in dfa_alphabet:
                new_state = []
                # if len(dfa_state) == 1 and (dfa_state[0], dfa_symbol) in self.transitions:
                #     #dfa_transitions[(dfa_state, dfa_symbol)] = self.transitions[(dfa_state[0], dfa_symbol)]
                #     for transition in self.transitions[(dfa_state[0], dfa_symbol)]:
                #         new_state.append(self.transitions[(transition, "eps")])
                #         dfa_transitions[(dfa_state, dfa_symbol)] = \
                #             self.transitions[(transition, "eps")]
                #
                #     if tuple(dfa_transitions[(dfa_state, dfa_symbol)]) not in dfa_states:
                #         dfa_states.append(tuple(dfa_transitions[(dfa_state, dfa_symbol)]))
                # else:
                for dfa_substate in dfa_state:
                    if (dfa_substate, dfa_symbol) in self.transitions and \
                            self.transitions[(dfa_substate, dfa_symbol)] not in new_state:
                        #new_state.append(self.transitions[(dfa_substate, dfa_symbol)])
                        for transition in self.transitions[(dfa_substate, dfa_symbol)]:
                            new_state.append(self.transitions[(transition, "eps")])

                if new_state:
                    new_state = list(chain.from_iterable(new_state))
                    dfa_transitions[(dfa_state, dfa_symbol)] = new_state

                    if tuple(new_state) not in dfa_states:
                        dfa_states.append(tuple(new_state))

        # Writing to JSON file.
        for key, value in dfa_transitions.items():
            temp_list = [["-".join(key[0]), key[1], "-".join(value)]]
            dfa_t_func.extend(temp_list)

        for dfa_state in dfa_states:
            for accepting_state in self.accepting_states:
                if accepting_state in dfa_state:
                    dfa_accepting_states.append("-".join(dfa_state))

        dfa = dict()
        dfa["states"] = len(dfa_states)
        dfa["alphabet"] = dfa_alphabet
        dfa["transitions"] = dfa_t_func
        dfa["initial_state"] = dfa_initial_state
        dfa["accepting_states"] = dfa_accepting_states

        with open(file_name, 'w') as f:
            json.dump(dfa, f)
