from neuroflow.core import get_parser, run_command


def main():
    parser = get_parser()
    args = parser.parse_args()
    run_command(args)


if __name__ == "__main__":
    main()
