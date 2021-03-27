from os.path import isdir, isfile, join
from string import Template

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

env.SConscript("_common.py")

FRAMEWORK_DIR = platform.get_package_dir("E21A")
assert isdir(FRAMEWORK_DIR)


def get_linker_script(mcu):
    ldscript = join(FRAMEWORK_DIR, "ldscripts", mcu[0:11].upper() + "_FLASH.ld")

    if isfile(ldscript):
        return ldscript

    default_ldscript = join(FRAMEWORK_DIR, "ldscripts", mcu[0:11].upper() + "_DEFAULT.ld")

    print("Warning! Cannot find a linker script for " + mcu[0:11].upper() + " with " + ldscript +
            ", Firmware will be linked with a default linker  " + default_ldscript)

    if isfile(default_ldscript):
        return default_ldscript

    ram = board.get("upload.maximum_ram_size", 0)
    flash = board.get("upload.maximum_size", 0)
    template_file = join(FRAMEWORK_DIR, "ldscripts", "tpl", "linker.tpl")
    content = ""
    with open(template_file) as fp:
        data = Template(fp.read())
        content = data.substitute(
            stack=hex(0x20000000 + ram), # 0x20000000 - start address for RAM
            ram=str(int(ram/1024)) + "K",
            flash=str(int(flash/1024)) + "K"
        )

    with open(default_ldscript, "w") as fp:
        fp.write(content)

    return default_ldscript

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, board.get("build.core"),
            "cmsis", "cores"),
        join(FRAMEWORK_DIR, board.get("build.core"), "cmsis",
            "variants", board.get("build.mcu")[0:7]),
        join(FRAMEWORK_DIR, board.get("build.core"),
            "variants", board.get("build.mcu")[0:7], "inc"),
        join(FRAMEWORK_DIR, board.get("build.core"),
            "variants", board.get("build.mcu")[0:7], "src")
    ]
)

env.Append(
    CPPDEFINES=[
        "USE_STDPERIPH_DRIVER"
    ]
)

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=get_linker_script(board.get("build.mcu")))

#
# Target: Build SPL Library
#

extra_flags = board.get("build.extra_flags", "")
src_filter_patterns = ["+<*>"]
if "STM32F40_41xxx" in extra_flags:
    src_filter_patterns += ["-<stm32f4xx_fmc.c>"]
    src_filter_patterns += ["-<startup_stm32f42xx.S>"]
    src_filter_patterns += ["-<startup_stm32f401x.S>"]
if "STM32F427_437xx" in extra_flags:
    src_filter_patterns += ["-<stm32f4xx_fsmc.c>"]
    src_filter_patterns += ["-<startup_stm32f40xx.S>"]
    src_filter_patterns += ["-<startup_stm32f401x.S>"]
elif "STM32F303xC" in extra_flags:
    src_filter_patterns += ["-<stm32f30x_hrtim.c>"]
elif "STM32L1XX_MD" in extra_flags:
    src_filter_patterns += ["-<stm32l1xx_flash_ramfunc.c>"]

libs = []

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkCMSISVariant"),
    join(
        FRAMEWORK_DIR, board.get("build.core"), "cmsis",
        "variants", board.get("build.mcu")[0:7]
    )
))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkSPL"),
    join(FRAMEWORK_DIR, board.get("build.core"),
        "variants", board.get("build.mcu")[0:7], "src"),
    src_filter=" ".join(src_filter_patterns)
))

env.Append(LIBS=libs)
