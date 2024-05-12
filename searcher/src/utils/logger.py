import subprocess
from os import system


def error(message, b, c):
    level = "error"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def warning(message, b, c):
    level = "warn"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def info(message, b, c):
    level = "info"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def debug(message, b, c):
    level = "debug"
    result = subprocess.run(["gum", "log", "-s", "-t", "TimeOnly", "-l",
                             level, message, b, c],
                            stdout=subprocess.PIPE, text=True)
    print(f"{result.stdout.strip()}")


def pretty_print(template, *args):
    parts = template.split('C')
    gum_template = ""
    for i, part in enumerate(parts):
        if i < len(args):
            gum_template += part + f'{{{{ Color "50" "0" " {args[i]} " }}}}'
        else:
            gum_template += part
    system(f"gum format -t template '{gum_template}'")


def format_traceback_line(tb_line):
    parts = tb_line.replace('"', '').replace(',', '').replace('\n', '').split(' ')
    file_name = parts[3]
    line_number = parts[5]
    module = parts[7]
    code = ' '.join(tb_line.split(' ')[8:])
    pretty_print("File C ", file_name)
    pretty_print("line C ", line_number)
    pretty_print("in C \n", module)
    system(f"gum format -t code -l python '{code}'")


def print_traceback(formated_exception):
    for i in range(1, len(formated_exception)-1):
        format_traceback_line(formated_exception[i])

    last_line = formated_exception[-1].replace('\n', '')
    error = last_line.split(':')
    error_desc = ' '.join(error[1:])
    pretty_print("C: C\n", error[0], error_desc)
