from nfa import *


def main():
    nfa = Nfa("nfa.json")
    nfa.convert_to_dfa("dfa.json")


if __name__ == "__main__":
    main()
