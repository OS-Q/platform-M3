from os.path import join

from SCons.Script import Import, SConscript

Import("env")

SConscript(
    join(env.PioPlatform().get_package_dir("framework-zephyr"), "scripts",
        "platformio", "platformio-build.py"), exports="env")
