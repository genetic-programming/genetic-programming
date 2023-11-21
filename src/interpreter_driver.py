from argparse import ArgumentParser
from pathlib import Path

from interpreter.interpreter import create_interpreter
from interpreter.language_types.integer import IntegerType


def main() -> None:
    """
    Runs interpreter on given file from /src/ directory.

    Example usages:
    $ python interpreter_driver.py ./example_programs/example1
    """

    parser = ArgumentParser()
    parser.add_argument(
        "source",
        metavar="source file name",
        type=str,
        nargs="?",
        default="./example_programs/example_1",
    )
    parser.add_argument(
        "--print-stacktraces",
        metavar="should stacktraces be printed in python convention",
        type=bool,
        nargs="?",
        default=False,
    )

    args = parser.parse_args()
    source_file_path = str(Path(__file__).parent / args.source)

    interpreter = create_interpreter(print_stacktraces=args.print_stacktraces)
    result = interpreter.interpret_file(file_path=source_file_path, inputs=[IntegerType(1), IntegerType(1)])
    print(result)  # noqa: T201


if __name__ == "__main__":
    main()
