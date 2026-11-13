import re
from models import Instruction, RailProgram


LABEL_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z_0-9]*$")


def parse_rail(source):
    instructions = []
    labels = {}

    for line_number, raw_line in enumerate(source.splitlines(), 1):
        line = raw_line.split(';', 1)[0].strip()
        if not line:
            continue

        if ':' in line:
            candidate, remainder = line.split(':', 1)
            label = candidate.strip()
            if label in labels:
                raise ValueError(f'В строке {line_number} повторное объявление метки {label}')
            labels[label] = len(instructions)
            line = remainder.strip()
            if not line:
                continue

        parts = line.split(None, 1)
        operation = parts[0].upper()
        args = [part.strip() for part in parts[1].split(',')]
        if len(args) != 3:
            raise ValueError(f'В строке {line_number} не 3 аргумента')
        instructions.append(Instruction(operation, (args[0], args[1], args[2]), line_number))

    return RailProgram(instructions=instructions, labels=labels)


def parse_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        source = file.read()
    return parse_rail(source)
