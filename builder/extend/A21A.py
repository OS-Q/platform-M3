import sys
from os.path import join, isfile

from SCons.Script import DefaultEnvironment, SConscript

env = DefaultEnvironment()
mcu = env.BoardConfig().get("build.mcu")
core = env.BoardConfig().get("build.core", "")

if core == "maple":
    build_script = join(
        env.PioPlatform().get_package_dir("A21B"),
        "tools", "build-%s.py" % mcu[0:7])
elif core == "stm32l0":
    build_script = join(
        env.PioPlatform().get_package_dir("A21C"),
        "tools", "build.py")
else:
    build_script = join(env.PioPlatform().get_package_dir(
        "A21A"), "tools", "build.py")

if not isfile(build_script):
    sys.stderr.write("Error: Missing PlatformIO build script %s!\n" % build_script)
    env.Exit(1)

SConscript(build_script)
