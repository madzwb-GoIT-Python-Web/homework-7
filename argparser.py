import argparse
# from pathlib import Path

import commands
import queries
import tools

parser = None
subparsers = None
exit_aliases = ["good","bye","good_bye","close"]

def create_parser():
    global parser
    global subparsers
    exit_on_error = False

    """Global parser options"""
    parser = argparse.ArgumentParser(
        exit_on_error = exit_on_error,
        description = "DB manipulation CLI.",
        formatter_class = argparse.RawTextHelpFormatter,
        # epilog = "HELP:\n\
    )

    parser.add_argument(
        "-c --connect --url",
        help = "Specify URL.",
        type = str,
        metavar = "url",
        dest = "url",
        default = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
        required=False
    )

    """Internal commands' parser"""
    subparsers = parser.add_subparsers(dest = "command")
    
    parser_create = subparsers.add_parser(
        "create",
        exit_on_error = exit_on_error,
        aliases = ["c", "insert", "i"],
        help = "Create record"
    )
    parser_create.add_argument(
        "model",
        help = "Model",
        type = str.lower,
        nargs = 1,
    )

    parser_create.add_argument(
        "values",
        help = "values",
        nargs = '+',
    )
    # parser_create.add_argument(
    #     "group",
    #     nargs = '?',
    #     help = "Group",
    #     default = "",
    # )
    # parser_create.add_argument(
    #     "id",
    #     nargs = '?',
    #     help = "Id",
    #     default = -1,
    # )
    parser_create.set_defaults(func = commands.create)
    # for action in parser_create._actions: # Hook - Positional options can't be unrequired
    #     action.required = False

    parser_read = subparsers.add_parser(
        "read",
        exit_on_error = exit_on_error,
        aliases = ["r", "select", "s", "list", "l"],
        help = "Read record(s)."
    )
    parser_read.add_argument(
        "model",
        help = "Model",
        type = str.lower,
        nargs = 1,
    )

    parser_read.add_argument(
        "filter",
        help = "Filter",
        nargs = '*',
        default = '',
    )

    parser_read.set_defaults(func = commands.read)
    # for action in parser_create._actions: # Hook - Positional options can't be unrequired
    #     action.required = False

    parser_update = subparsers.add_parser(
        "update",
        exit_on_error = exit_on_error,
        aliases = ["u"],
        help = "Update record."
    )
    parser_update.add_argument(
        "model",
        help = "Model",
        type = str.lower,
        nargs = 1,
    )
    parser_update.add_argument(
        "filter",
        help = "Filter",
        nargs = 1,
    )
    # parser_update.add_argument(
    #     "id",
    #     nargs = 1,
    #     help = "Id",
    #     default = -1,
    # )
    parser_update.add_argument(
        "values",
        help = "values",
        nargs = '+',
    )
    parser_update.set_defaults(func = commands.update)
    # for action in parser_create._actions: # Hook - Positional options can't be unrequired
    #     action.required = False

    parser_delete = subparsers.add_parser(
        "delete",
        exit_on_error = exit_on_error,
        aliases = ["d", "remove"],
        help = "Delete record."
    )
    parser_delete.add_argument(
        "model",
        help = "Model",
        type = str.lower,
        nargs = 1,
    )
    parser_delete.add_argument(
        "filter",
        help = "Filter",
        nargs = '+',
    )
    # parser_update.add_argument(
    #     "id",
    #     nargs = '?',
    #     help = "Id",
    #     # default = -1,
    # )
    parser_delete.set_defaults(func = commands.delete)
    # for action in parser_create._actions: # Hook - Positional options can't be unrequired
    #     action.required = False

    parser_hello = subparsers.add_parser(
        "hello",
        exit_on_error = exit_on_error,
        aliases = ["h", "hi"],
        help = "Hello"
    )
    parser_hello.set_defaults(func = commands.hello)

    parser_bye = subparsers.add_parser(
        "exit",
        exit_on_error = exit_on_error,
        aliases = exit_aliases,
        help = "Exit"
    )
    parser_bye.set_defaults(func = commands.bye)

    parser_sql = subparsers.add_parser(
        "sql",
        exit_on_error = exit_on_error,
        # aliases = ["d", "remove"],
        help = "Execute SQL."
    )
    parser_sql.add_argument(
        "sql",
        help = "SQL"
    )
    parser_sql.set_defaults(func = commands.sql)
    # for action in parser_create._actions: # Hook - Positional options can't be unrequired
    #     action.required = False
    for name, query in queries.registry.items():
        subparser = subparsers.add_parser(
                        name,
                        exit_on_error = exit_on_error,
                        # aliases = ["d", "remove"],
                        help = "Execute " + name + ".",
                    )
        subparser.add_argument(
            "filter",
            help = "Filter",
            nargs = '*',
            default = '',
        )
        subparser.set_defaults(func = query)



def check_exit(command, aliases = exit_aliases) -> bool:
    return command in aliases or command == "exit"

"""Parse command line"""
def parse_command(command: str) -> list:
    commands = tools.tokenize(command)
    # commands = re.split("\"|\'", command) # For correct parsing options enclosed by " or '
    # if len(commands) == 1: # If no options enclosed by " or ', try by space
    #     commands = re.split(" ", command)
    # results = []
    # skip = False
    # for c in commands:
    #     if skip:
    #         skip = False
    #         results.append(c)
    #         continue
    #     if not c or c in " ":
    #         skip = True
    #         continue
    #     cc = re.split(" ", c)
    #     results.extend(cc)
    commands = list(map(lambda x: x.strip(), commands))
    commands = list(filter(lambda x: len(x), commands)) # Remove empties
    return commands

def parse_commands(commands: list, _parser: argparse.ArgumentParser|None = None):
    if _parser is None:
        _parser = parser
    result = None
    parsed_commands = None
    # for command in commands:
    try:
        parsed_commands = _parser.parse_args(commands)
    except SystemExit as e: # Hook
        result =  ""
    except argparse.ArgumentError as e:
        result = e
    # Execute command
    if parsed_commands:
        result = parsed_commands.func(parsed_commands)
        if result is not None:
            tools.print_result(result)
    return parsed_commands
