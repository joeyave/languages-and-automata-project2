import json
from itertools import chain


def epsilon_closure(state, transitions):
    closure = []
    for substate in state:
        if (substate, "eps") in transitions:
            closure.append(substate)
            closure.extend(epsilon_closure(transitions[(substate, "eps")], transitions))
        if substate not in closure:
            closure.append(substate)
    return closure


class Nfa:
    def __init__(self, file_name):
        with open(file_name, 'r') as f:
            nfa_dict = json.load(f)

        self.alphabet = nfa_dict['alphabet']
        self.transitions = {}
        for transition in nfa_dict['transitions']:
            self.transitions[(transition[0], transition[1])] = transition[2]
        self.initial_state = nfa_dict['initial_state']
        self.accepting_states = nfa_dict['accepting_states']

    def convert_to_dfa(self, file_name):
        dfa_alphabet = self.alphabet
        dfa_t_func = []
        dfa_initial_state = epsilon_closure([self.initial_state], self.transitions)
        dfa_accepting_states = []
        dfa_states = [tuple(dfa_initial_state)]

        dfa_transitions = {}

        for dfa_state in dfa_states:
            for dfa_symbol in dfa_alphabet:
                new_state = []
                for dfa_substate in dfa_state:
                    if (dfa_substate, dfa_symbol) in self.transitions and \
                            self.transitions[(dfa_substate, dfa_symbol)] not in new_state:
                        for transition in self.transitions[(dfa_substate, dfa_symbol)]:
                            epsilon_transition_state = epsilon_closure([transition], self.transitions)
                            if epsilon_transition_state not in new_state:
                                new_state.append(epsilon_transition_state)
                            # if self.transitions[(transition, "eps")] not in new_state:
                            #     new_state.append(self.transitions[(transition, "eps")])

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
        dfa["alphabet"] = dfa_alphabet
        dfa["transitions"] = dfa_t_func
        dfa["initial_state"] = "-".join(dfa_initial_state)
        dfa["accepting_states"] = dfa_accepting_states

        with open(file_name, 'w') as f:
            json.dump(dfa, f)
