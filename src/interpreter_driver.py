from argparse import ArgumentParser
from pathlib import Path

from gp_algorithm.interpreter.interpreter import Interpreter


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
        default="example.txt",
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

    interpreter = Interpreter()
    program_input = interpreter.interpret_input(input_strings=["1001", "200"])
    result = interpreter.interpret_file(
        file_path=source_file_path,
        program_input=program_input,
    )
    print(result)  # noqa: T201


if __name__ == "__main__":
    main()
