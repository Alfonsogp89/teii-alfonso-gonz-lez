import getopt
import sys


def usage():
    print(f"Uso: {sys.argv[0]}: [-o OUTPUT] [-v] [-h]")


def parse_options():
    args = dict()
    args["output"] = None
    args["verbose"] = False

    try:
        options, _ = getopt.getopt(sys.argv[1:], "o:vh", ["output=", "verbose", "help"])
    except getopt.GetoptError as error:
        print(error)
        usage()
        sys.exit(2)

    for option, argument in options:
        if option:
            if option in ("-o", "--output"):
                args["output"] = argument
            elif option in ("-v", "--verbose"):
                args["verbose"] = True
            elif option in ("-h", "--help"):
                usage()
                sys.exit()
            else:
                usage()
                sys.exit(2)
    return args


def main():
    args = parse_options()
    print(f"args: {args}")


if __name__ == "__main__":
    main()
