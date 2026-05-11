import click


@click.command()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Enable verbose output')
@click.option('-o', '--output',  help='Output.')
def main(output, verbose):
    print(f"args: output: {output}, verbose: {verbose}")


if __name__ == "__main__":
    main()
