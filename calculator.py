import difflib

from imx477.nvidia import (
    imx477_mode_1920x1080_60fps,
    imx477_mode_4032x3040_30fps
)
from imx477.raspberry import mode_4056x3040_regs_10fps
from imx477.zenqberry import sensor_4k_regs_30fps_10b
from imx477.registers import add_label, NAME_TO_VALUE


def add_register_labels(registers_list):
    for register, value in registers_list:
        yield f"{add_label(register)} => {str(value).rjust(10)} ({hex(value)})"


if __name__ == "__main__":
    low_res_mode = list(add_register_labels(sorted(imx477_mode_4032x3040_30fps)))
    # print(low_res_mode)

    high_res_mode = list(add_register_labels(sorted(mode_4056x3040_regs_10fps)))
    # print(high_res_mode)

    zynqberry = list(add_register_labels(sorted(mode_4056x3040_regs_10fps)))
    # print(high_res_mode)

    rpi_mod = list(add_register_labels(sorted(mode_4056x3040_regs_10fps)))
    # print(high_res_mode)

    # diff = difflib.ndiff(zynqberry, rpi_mod)
    # print('\n'.join(diff))

    print('\n'.join(rpi_mod))

    # external frequency, e.g. 24mhz
    external_clk = 24000000 / 2
    print(f"external_clk = {external_clk}")
    registers = dict(mode_4056x3040_regs_10fps)

    pre_iop_div_reg = NAME_TO_VALUE['REG_IVT_PREPLLCK_DIV']
    pre_iop_div = registers[pre_iop_div_reg]

    iop_mphy_reg_msb = NAME_TO_VALUE['REG_IOP_MPY_MSB']
    iop_mphy_reg_lsb = NAME_TO_VALUE['REG_IOP_MPY_LSB']
    iop_mphy = (registers[iop_mphy_reg_msb] << 8) | registers[iop_mphy_reg_lsb]

    iop_syck_div_reg = NAME_TO_VALUE['REG_IOPSYCK_DIV']
    iop_pxck_div_reg = NAME_TO_VALUE['REG_IOPPXCK_DIV']

    iop_syck_div = registers[iop_syck_div_reg]
    iop_pxck_div = registers[iop_pxck_div_reg]

    print(f"iop_prepllck_div = {pre_iop_div}")
    print(f"iop_pll_mphy = {iop_mphy}")
    print(f"iopck (LINK_FREQ) = {external_clk / pre_iop_div * iop_mphy}")
    print()

    print(f"iop_syck_div = {iop_syck_div}")
    print(f"iop_pxck_div = {iop_pxck_div}")

    print(f"ioppxck = {(external_clk / pre_iop_div * iop_mphy) / (iop_syck_div * iop_pxck_div)}")


    ivt_prepllck_div_reg = NAME_TO_VALUE['REG_IVT_PREPLLCK_DIV']
    ivt_prepllck_div = registers[ivt_prepllck_div_reg]

    ivt_mphy_reg_msb = NAME_TO_VALUE['REG_PLL_IVT_MPY_MSB']
    ivt_mphy_reg_lsb = NAME_TO_VALUE['REG_PLL_IVT_MPY_LSB']
    ivt_mphy = (registers[ivt_mphy_reg_msb] << 8) | registers[ivt_mphy_reg_lsb]


    ivt_syck_div_reg = NAME_TO_VALUE['REG_IVTSYCK_DIV']
    ivt_pxck_div_reg = NAME_TO_VALUE['REG_IVTPXCK_DIV']

    ivt_syck_div = registers[iop_syck_div_reg]
    ivt_pxck_div = registers[iop_pxck_div_reg]



    print(f"ivt_prepllck_div = {ivt_prepllck_div}")
    print(f"ivt_pll_mphy = {ivt_mphy}")
    print(f"adck = {external_clk / ivt_prepllck_div * ivt_mphy}")


    print(f"adck = {(external_clk / pre_iop_div * iop_mphy) / (iop_syck_div * iop_pxck_div)}")


    print(f"ivtpxck = {(external_clk / ivt_prepllck_div * ivt_mphy) / (ivt_syck_div * ivt_pxck_div)}")
    print(f"iop_pxck_div = {iop_pxck_div}")

    print()
    print(f"LINK_FREQ = {external_clk / pre_iop_div * iop_mphy}")
    print(f"PIXEL_RATE = {external_clk * ivt_mphy / 5}")




