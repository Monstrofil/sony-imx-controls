import argparse
import difflib

from imx477 import nvidia, raspberry, zenqberry
from imx577 import orangepi

from imx477.registers import add_label, NAME_TO_VALUE

modules = [nvidia, raspberry, zenqberry, orangepi]


def add_register_labels(registers_list):
    for register, value in registers_list:
        yield f"{add_label(register)} => {str(value).rjust(10)} ({hex(value)})"


def find_mode(name: str):
    for module in modules:
        for (mode_name, registers) in module.modes:
            if f'{module.__name__}.{mode_name}' == name:
                return registers

    raise FileNotFoundError('Unabme to find %s' % name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    available_choices = [
        f'{module.__name__}.{mode_name}'
        for module in modules
        for (mode_name, _) in module.modes
    ]

    parser.add_argument("-l", "--left", choices=available_choices, required=True)
    parser.add_argument("-r", "--right", choices=available_choices, required=True)

    args = parser.parse_args()

    low_res_mode = list(add_register_labels(sorted(find_mode(args.left))))
    high_res_mode = list(add_register_labels(sorted(find_mode(args.right))))

    diff = difflib.ndiff(low_res_mode, high_res_mode)
    print('\n'.join(diff))

