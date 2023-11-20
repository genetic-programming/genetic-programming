from argparse import ArgumentParser
from pathlib import Path

from antlr4 import ParseTreeWalker, TokenStream

from interpreter.interpreter import Interpreter
from interpreter.listener import Listener
from interpreter.recognizers import CustomLexer, CustomParser
from interpreter.variable_stack import VariableStack
from interpreter.visitors.main import Visitor


def main(
    file_path: str,
    allow_prints: bool,
    print_stacktraces: bool,
) -> None:
    variable_stack = VariableStack()
    interpreter = Interpreter(
        CustomLexer(),
        CustomParser(input=TokenStream()),
        Listener(variable_stack=variable_stack),
        ParseTreeWalker(),
        Visitor(variable_stack=variable_stack, allow_prints=allow_prints),
        print_stacktraces,
    )
    interpreter.interpret_file(file_path)


if __name__ == "__main__":
    """
    Runs interpreter on given file from /src/ directory.

    Example usages:
    $ python driver.py
    $ python driver.py ./example_programs/example1
    $ python driver.py ./example_programs/example2
    $ python driver.py ./example_programs/example3 --allow-prints true
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
        "--allow-prints",
        metavar="is prints allowed in code",
        type=bool,
        nargs="?",
        default=False,
    )
    parser.add_argument(
        "--print-stacktraces",
        metavar="should stacktraces be printed in python convention",
        type=bool,
        nargs="?",
        default=False,
    )

    args = parser.parse_args()
    source_file_path = Path(__file__).parent / args.source
    main(
        file_path=str(source_file_path),
        allow_prints=args.allow_prints,
        print_stacktraces=args.print_stacktraces,
    )
