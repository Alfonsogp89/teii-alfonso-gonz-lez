import argparse


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    return args


def main():
    args = parse_options()
    print(f"args: {args}")


if __name__ == "__main__":
    main()
