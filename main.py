import difflib

from imx477.nvidia import (
    imx477_mode_1920x1080_60fps,
    imx477_mode_4032x3040_30fps
)
from imx477.raspberry import mode_4056x3040_regs_10fps
from imx477.zenqberry import sensor_4k_regs_30fps_10b
from imx477.registers import add_label


def add_register_labels(registers_list):
    for register, value in registers_list:
        yield f"{add_label(register)} => {str(value).rjust(10)} ({hex(value)})"


if __name__ == "__main__":
    low_res_mode = list(add_register_labels(sorted(imx477_mode_4032x3040_30fps)))
    # print(low_res_mode)

    high_res_mode = list(add_register_labels(sorted(sensor_4k_regs_30fps_10b)))
    # print(high_res_mode)

    diff = difflib.ndiff(low_res_mode, high_res_mode)
    print('\n'.join(diff))

    # print('\n'.join(high_res_mode))