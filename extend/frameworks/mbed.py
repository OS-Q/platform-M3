from os.path import join

from SCons.Script import Import, SConscript

Import("env")

# https://github.com/platformio/builder-framework-mbed.git
SConscript(
    join(env.PioPlatform().get_package_dir("framework-mbed"), "platformio",
         "platformio-build.py"))
