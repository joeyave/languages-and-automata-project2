from nfa import *


def main():
    file_name = input("nfa/")
    nfa = Nfa("nfa/" + "".join(file_name))
    file_name = "d" + file_name[1:]
    nfa.convert_to_dfa("dfa/" + "".join(file_name))


if __name__ == "__main__":
    main()
